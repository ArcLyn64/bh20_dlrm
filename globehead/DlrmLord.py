import random

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

class Lord:

    def __init__(self, bs, t):
        self.board_size = bs
        self.team = t
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        self.spawnrow = 0 if self.team == Team.WHITE else self.board_size-1
        self.targetrow = self.board_size-1 if self.team == Team.WHITE else 0
        self.forward = 1 if self.team == Team.WHITE else -1
        self.left = self.forward * 1
        self.right = self.forward * -1

    def board(self):
        return get_board()

    def check_space(self, r, c):
        if not self.check_inbounds(r, c):
            return False
        try:
            return check_space(r, c)
        except:
            return None

    def check_inbounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def score_col(self, c):
        if self.check_space(self.targetrow, c) == self.team:
            return -1 # we finished this row, naive row by row strat doesn't want to use it
        loc = self.spawnrow + 1
        for dist in range(self.board_size, 1, -1):
            check = self.check_space(loc, c)
            if check == self.team:
                return 0
            if check == self.opp_team:
                return dist ** 2
            loc += self.forward
        return 1

    def try_spawn(self, c):
        if not self.check_space(self.spawnrow, c):
            spawn(self.spawnrow, c)
            return True
        return False

    def turn(self):
        scores = [(self.score_col(c), c) for c in range(self.board_size)] 
        # sorts in place by highest score first, then orders equal scores randomly
        scores.sort(reverse=True, key=lambda x:(x[0], random.randint(0, self.board_size)))
        dlog("scores: " + str(scores))
        for _,c in scores:
            if self.try_spawn(c): break
