import random

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

# Pawn class things
VIEW_DIST = 2
RANGE = 5

class Pawn:

    WAIT_BEFORE_CAPTURE = 5
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
    
    """
    ------------------------------------------------------------
    Generated Functions Below
    ------------------------------------------------------------
    """

