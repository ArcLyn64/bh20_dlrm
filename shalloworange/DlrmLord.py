DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

class Lord:

    def __init__(self, bs, t, b):
        self.board_size = bs
        self.team = t
        self.board = b
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
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

    def score_col(self, c):
        if self.check_space_w(self.targetrow, c) == self.team:
            return -1 # we finished this row, naive row by row strat doesn't want to use it
        loc = self.spawnrow + 1
        for dist in range(self.board_size, 1, -1):
            check = self.check_space_w(loc, c)
            if check == self.team:
                return 0
            if check == self.opp_team:
                return dist ** 2
            loc += self.forward
        return 1

    def try_spawn(self, c):
        if not self.check_space_w(self.spawnrow, c):
            spawn(self.spawnrow, c)
            return True
        return False

    def turn(self):
        scores = [(self.score_col(c), c) for c in range(self.board_size)]
        scores.sort(reverse=True) # sorts in place by highest score first, then high col to low col
        dlog("scores: " + str(scores))
        for _,c in scores:
            if self.try_spawn(c): break
