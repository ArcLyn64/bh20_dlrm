import random

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

class Lord:
    SPACING = 2
    PULSE = 3
    IGNORE = 7
    INDEX = 2

    def __init__(self, bs, t):
        self.board_size = bs
        self.team = t
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        self.spawnrow = 0 if self.team == Team.WHITE else self.board_size-1
        self.targetrow = self.board_size-1 if self.team == Team.WHITE else 0
        self.forward = 1 if self.team == Team.WHITE else -1
        self.left = self.forward * 1
        self.right = self.forward * -1
        self.round = 0
        self.targets = self.generate_targets()

    def pillar_influence(self):
        return 1 + self.SPACING

    def generate_targets(self):
        start = self.INDEX + 1
        end = self.board_size - self.IGNORE + self.INDEX
        spaces = list(range(start, end, self.pillar_influence()))
        arr = []
        for s in spaces:
            for _ in range(self.PULSE):
                arr.append(s)
        return arr

    def board(self):
        return get_board()

    def check_space(self, r, c):
        if not self.check_inbounds(r, c):
            return False
        try:
            return check_space(r, c)
        except:
            return None

    def check_loc(self, loc):
        return self.check_space(loc[0], loc[1])

    def check_inbounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def space_safe(self, r, c):
        """
        A space is safe if it is protected by an ally or not attacked by an enemy
        """
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

    def score_col(self, c):
        if self.check_space(self.targetrow, c) == self.team:
            return -1 # we finished this row, naive row by row strat doesn't want to use it
        if not self.space_safe(self.spawnrow, c):
            return -2 # don't waste a turn getting immediately killed
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
        self.round = self.round + 1
        for i in range(0, self.pillar_influence()):
            for _ in self.targets:
                c = self.targets[self.round % len(self.targets)]
                c = (c + i) % self.board_size
                if c < self.INDEX: c += self.INDEX
                if self.try_spawn(c): return
                self.round = self.round + 1
