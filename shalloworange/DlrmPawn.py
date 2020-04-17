DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

class Pawn:

    def __init__(self, bs, t, l):
        self.board_size = bs
        self.team = t
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        self.loc = l
        self.spawnrow = 0 if self.team == Team.WHITE else self.board_size-1
        self.targetrow = self.board_size-1 if self.team == Team.WHITE else 0
        self.forward = 1 if self.team == Team.WHITE else -1
        self.left = self.forward * 1
        self.right = self.forward * -1

    def check_space_w(self, r, c):
        if not self.check_inbounds(r, c):
            return False
        try:
            return check_space(r, c)
        except:
            return None

    def check_inbounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def try_move(self):
        r, c = self.loc
        r += self.forward
        if self.check_inbounds(r, c) and not self.check_space_w(r, c):
            move_forward()
            return True
        return False

    def try_capture_left(self):
        return self.try_capture(False)

    def try_capture_right(self):
        return self.try_capture(True)

    def try_capture(self, isRight):
        r, c = self.loc
        r += self.forward
        c += self.right if isRight else self.left
        if self.check_space_w(r, c) == self.opp_team:
            capture(r, c)
            return True
        return False

    def turn(self):
        if self.try_capture_left(): return True
        if self.try_capture_right(): return True
        return self.try_move()
