import random

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

VIEW_DIST = 2

class Pawn:

    def __init__(self, bs, t):
        self.board_size = bs
        self.team = t
        self.opp_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        self.spawnrow = 0 if self.team == Team.WHITE else self.board_size-1
        self.targetrow = self.board_size-1 if self.team == Team.WHITE else 0
        self.forward = 1 if self.team == Team.WHITE else -1
        self.left = self.forward * 1
        self.right = self.forward * -1

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

    def can_move(self):
        r, c = self.loc()
        r += self.forward
        return self.check_inbounds(r, c) and not self.check_space(r, c)

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

    def can_capture_left(self):
        return self.can_capture(False)

    def try_capture_left(self):
        return self.try_capture(False)

    def can_capture_right(self):
        return self.can_capture(True)

    def try_capture_right(self):
        return self.try_capture(True)

    def can_capture(self, isRight):
        r, c = self.loc()
        r += self.forward
        c += self.right if isRight else self.left
        return self.check_space(r, c) == self.opp_team

    def try_capture(self, isRight):
        r, c = self.loc()
        r += self.forward
        c += self.right if isRight else self.left
        if self.can_capture(isRight):
            capture(r, c)
            return True
        return False

    def wait(self):
        """
        do nothing
        always succeeds
        """
        return True

    def check_doubled(self):
        r, c = self.loc()
        r -= self.forward
        return self.check_space(r, c) == self.team

    """
    Scoring
    """

    WAIT_SCORE = 0
    CAPTURE_VALUE = 6
    DANGER_VALUE = -3
    MOVE_VALUE = 2

    def score_action(self, action):
        """
        takes in one of the following:
            try_capture_left
            try_capture_right
            try_move
            wait
        and scores the quality of that action
        wait is a default action taken only when all other options are bad
        """
        d = {}
        d[self.try_capture_left] = self.score_capture_left
        d[self.try_capture_right] = self.score_capture_right
        d[self.try_move] = self.score_move
        d[self.wait] = self.score_wait
        return d[action]()

    def score_capture_left(self):
        return self.score_capture(False)

    def score_capture_right(self):
        return self.score_capture(True)

    def score_capture(self, isRight):
        r, c = self.loc()
        r += self.forward
        c += self.right if isRight else self.left
        score = self.CAPTURE_VALUE
        if not self.space_safe(r, c): score += self.DANGER_VALUE
        return score

    def score_move(self):
        r, c = self.loc()
        r += self.forward
        score = self.MOVE_VALUE
        if not self.space_safe(r, c): score += self.DANGER_VALUE
        return score

    def score_wait(self):
        return self.WAIT_SCORE

    def log_scores(self, scores):
        d = {}
        d[self.try_capture_left] = "cap left"
        d[self.try_capture_right] = "cap right"
        d[self.try_move] = "move"
        d[self.wait] = "wait"
        scores = [(s[0], d[s[1]]) for s in scores]
        dlog("scores: " + str(scores))



    def turn(self):
        actions = [self.wait]
        if self.can_capture_left(): actions.append(self.try_capture_left)
        if self.can_capture_right(): actions.append(self.try_capture_right)
        if self.can_move(): actions.append(self.try_move)
        scores = [(self.score_action(a), a) for a in actions]
        # sort by highest score, then randomly
        scores.sort(reverse=True, key=lambda x:(x[0], random.randint(0, len(actions))))
        self.log_scores(scores)
        for _,a in scores:
            if a(): break
