import random

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

class Patterns:
    """
    Use 's' for self because it won't get checked for that way (is implied)

    formatting for pattern recognition:
    all done from black's perspective (up is forward)
    """
    CHAIN_SHORT_LEFT = [
            str.split(". . . . ."),
            str.split(". O . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_SHORT_RIGHT = [
            str.split(". . . . ."),
            str.split(". . . O ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_LONG_LEFT = [
            str.split("O . . . ."),
            str.split(". O . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_LONG_RIGHT = [
            str.split(". . . . O"),
            str.split(". . . O ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    SPEAR_TIP = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". O . O ."),
            str.split(". . . . .")
            ]

    CAP_LEFT = [
            str.split(". . . . ."),
            str.split(". X . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CAP_RIGHT = [
            str.split(". . . . ."),
            str.split(". . . X ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CAN_MOVE = [
            str.split(". . . . ."),
            str.split(". . _ . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    STALEMATE_LEFT = [
            str.split(". X . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    STALEMATE_RIGHT = [
            str.split(". . . X ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    BLOCKED = [
            str.split(". . . . ."),
            str.split(". . X . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

"""
----------------------------------------------------------
"""

# Pawn class things
VIEW_DIST = 2
RANGE = 5

class Pawn:

    WAIT_BEFORE_CAPTURE = 5

    def generate_check_position_function(self, *argv):
        """
        Takes in any number of 5x5 matrix that indicates the total viewspace of the pawn
        X are enemies
        O are friendlies
        _ are empty spaces
        anything else we don't care about
        generates a function which checks if we match any of those patterns
        """
        ENEMY = 'X'
        FRIEND = 'O'
        EMPTY = '_'
        functions = []
        for mat in argv:
            bool_checks = []
            for i in range(RANGE):
                for j in range(RANGE):
                    r = (VIEW_DIST - i) * self.forward
                    c = (VIEW_DIST - j) * self.forward
                    if mat[i][j] == ENEMY:
                        bool_checks.append(lambda y, x: (self.check_space(y + r, x + c) == self.opp_team))
                    if mat[i][j] == FRIEND:
                        bool_checks.append(lambda y, x: (self.check_space(y + r, x + c) == self.team))
                    if mat[i][j] == EMPTY:
                        bool_checks.append(lambda y, x: (self.check_space(y + r, x + c) == None))
            functions.append(lambda r, c: any([b(r, c) for b in bool_checks]))
        def full_check():
            r, c = self.loc()
            return any([f(r, c) for f in functions])
        dlog("completed a run!")
        return full_check

    def __init__(self, bs, t):
        self.board_size = bs
        self.team = t
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        self.spawnrow = 0 if self.team == Team.WHITE else self.board_size-1
        self.targetrow = self.board_size-1 if self.team == Team.WHITE else 0
        self.forward = 1 if self.team == Team.WHITE else -1
        self.left = self.forward * 1
        self.right = self.forward * -1
        self.capture_timer = self.WAIT_BEFORE_CAPTURE
        self.action = self.march

        """
        Generate pattern functions
        """
        gpf = self.generate_check_position_function # alias for brevity
        self.can_capture_left = gpf(Patterns.CAP_LEFT)
        self.can_capture_right = gpf(Patterns.CAP_RIGHT)
        self.can_move = gpf(Patterns.CAN_MOVE)

    def loc(self):
        return get_location()

    def check_space(self, r, c):
        if not self.check_inbounds(r, c) or not self.check_inview(r, c):
            return False
        try:
            return check_space(r, c)
        except:
            return None

    def check_loc(self, loc):
        return self.check_space(loc[0], loc[1])

    def check_inbounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def check_inview(self, r, c):
        rpos, cpos = self.loc()
        return -VIEW_DIST <= r - rpos <= VIEW_DIST and -VIEW_DIST <= c-cpos <= VIEW_DIST

    def try_move(self):
        if self.can_move():
            move_forward()
            return True
        return False

    def space_safe(self, r, c):
        """
        A space is safe if it is protected by an ally or not attacked by an enemy
        """
        if not self.check_inview(r, c):
            return None
        # check if the space is defended by friendly pawn
        friend_left = (r - self.forward, c + self.left)
        friend_right = (r - self.forward, c + self.right)
        if self.check_loc(friend_left) == self.team or self.check_loc(friend_right) == self.team:
            return True
        # check if the space is under attack
        enemy_left = (r + self.forward, c + self.left)
        enemy_right = (r + self.forward, c + self.right)
        if self.check_loc(enemy_left) == self.opp_team or self.check_loc(enemy_right) == self.opp_team:
            return False
        return True

    def try_capture_left(self):
        if self.can_capture_left():
            return capture(r + self.forward, r + self.left)
        return False;

    def try_capture_right(self):
        if self.can_capture_right():
            return capture(r + self.forward, r + self.right)
        return False;

    def wait(self):
        """
        do nothing
        always succeeds
        """
        return True

    def should_move(self):
        """
        Checks if we should move forward (can move and space safe)
        """
        r, c = self.loc()
        return self.can_move() and self.space_safe(r+self.forward, c)

    def turn(self):
        self.action = self.action()

    def march(self):
        protocol = [self.try_capture_left, self.try_capture_right, self.should_move, self.wait]
        for a in protocol:
            if a(): break
        return self.march
