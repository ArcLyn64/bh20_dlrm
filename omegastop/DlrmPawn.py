import random
import bh_util as util

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
        self.action = self.combat if self.enemy_spotted else self.advance

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
        r, c = self.loc()
        if self.can_capture_left():
            return capture(r + self.forward, r + self.left)
        return False;

    def try_capture_right(self):
        r, c = self.loc()
        if self.can_capture_right():
            return capture(r + self.forward, r + self.right)
        return False;

    def try_capture(self):
        return self.try_capture_left() or self.try_capture_right()

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
        # only play aggressive if you're on an even column
        if self.can_move() and ((c%2==0 and self.move_defended()) or not self.move_attacked()):
            return self.try_move()
        return False

    def turn(self):
        self.action = self.action()

    def advance(self):
        self.try_move()
        return self.state_manager(self.advance)

    def combat(self):
        acted = False
        if not acted and not self.move_attacked() and self.can_move_to_defend():
            acted = self.try_move()
        if not acted:
            acted = self.try_capture()
        if not acted and not self.move_attacked():
            acted = self.try_move()
        if not acted:
            acted = self.wait()
        return self.state_manager(self.combat)

    def finished(self):
        wait()
        return self.state_manager(self.finished)

    def threaten(self):
        if self.can_capture_left():
            self.try_capture_left()
        elif self.can_capture_right():
            self.try_capture_right()
        elif not self.can_move():
            self.capture_timer = 0
        elif self.short_chain_ahead():
            self.try_move()
        elif self.capture_timer <= 0:
            self.try_move()
        else:
            self.capture_timer = self.capture_timer - 1
        return self.state_manager(self.threaten)

    def state_manager(self, state):
        r, c = self.loc()
        if c == self.targetrow:
            return self.finished
        if c == self.targetrow - self.forward:
            return self.threaten
        if state == self.combat or self.enemy_spotted():
            return self.combat
        if state == self.advance:
            return self.advance
        return self.combat # default is to assume danger

    
    """
    ------------------------------------------------------------
    Generated Functions Below
    ------------------------------------------------------------
    """

# New Write, make sure to delete any above writes to avoid duplicate definitions
    def can_move(self):
        r, c = self.loc()
        return (not self.check_space(r + self.forward, c))

    def can_capture_left(self):
        r, c = self.loc()
        return (self.check_space(r + self.forward, c + self.left) == self.opp_team)

    def can_capture_right(self):
        r, c = self.loc()
        return (self.check_space(r + self.forward, c + self.right) == self.opp_team)

    def move_attacked(self):
        r, c = self.loc()
        return (self.check_space(r + (2*self.forward), c + self.left) == self.opp_team) or \
        (self.check_space(r + (2*self.forward), c + self.right) == self.opp_team)

    def move_defended(self):
        r, c = self.loc()
        return (self.check_space(r, c + self.left) == self.team) or \
        (self.check_space(r, c + self.right) == self.team)

    def can_move_to_defend(self):
        r, c = self.loc()
        return (self.check_space(r + (2*self.forward), c + self.left) == self.team and \
        not self.check_space(r + self.forward, c)) or \
        (self.check_space(r + (2*self.forward), c + self.right) == self.team and \
        not self.check_space(r + self.forward, c))

    def can_move_to_trade(self):
        r, c = self.loc()
        return (self.check_space(r + (2*self.forward), c + self.left) == self.opp_team and \
        not self.check_space(r + self.forward, c) and \
        self.check_space(r, c + self.left) == self.team) or \
        (self.check_space(r + (2*self.forward), c + self.right) == self.opp_team and \
        not self.check_space(r + self.forward, c) and \
        self.check_space(r, c + self.left) == self.team) or \
        (self.check_space(r + (2*self.forward), c + self.right) == self.opp_team and \
        not self.check_space(r + self.forward, c) and \
        self.check_space(r, c + self.right) == self.team) or \
        (self.check_space(r + (2*self.forward), c + self.left) == self.opp_team and \
        not self.check_space(r + self.forward, c) and \
        self.check_space(r, c + self.right) == self.team)

    def enemy_spotted(self):
        r, c = self.loc()
        return (self.check_space(r + (2*self.forward), c + (2*self.left)) == self.opp_team) or \
        (self.check_space(r + (2*self.forward), c + self.left) == self.opp_team) or \
        (self.check_space(r + (2*self.forward), c + (2*self.right)) == self.opp_team) or \
        (self.check_space(r + (2*self.forward), c + self.right) == self.opp_team)

    def short_chain_ahead(self):
        r, c = self.loc()
        return (self.check_space(r + self.forward, c + self.left) == self.team) or \
        (self.check_space(r + self.forward, c + self.right) == self.team)

    def long_chain_ahead(self):
        r, c = self.loc()
        return (self.check_space(r + (2*self.forward), c + (2*self.left)) == self.team and \
        self.check_space(r + self.forward, c + self.left) == self.team) or \
        (self.check_space(r + (2*self.forward), c + (2*self.right)) == self.team and \
        self.check_space(r + self.forward, c + self.right) == self.team)

    def short_chain_behind(self):
        r, c = self.loc()
        return (self.check_space(r + (-1*self.forward), c + self.left) == self.team) or \
        (self.check_space(r + (-1*self.forward), c + self.right) == self.team)

    def long_chain_behind(self):
        r, c = self.loc()
        return (self.check_space(r + (-1*self.forward), c + self.left) == self.team and \
        self.check_space(r + (-2*self.forward), c + (2*self.left)) == self.team) or \
        (self.check_space(r + (-1*self.forward), c + self.right) == self.team and \
        self.check_space(r + (-2*self.forward), c + (2*self.right)) == self.team)

    def blocked(self):
        r, c = self.loc()
        return (self.check_space(r + self.forward, c) == self.opp_team)

