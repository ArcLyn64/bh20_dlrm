

DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

def turn():
    if get_type() == RobotType.PAWN:
        pawn_turn(get_board_size(), get_team(), get_location())
    else:
        lord_turn(get_board_size(), get_team(), get_board())


"""
PAWN THINGS TO DO
"""

def check_space_w(r, c, board_size):
    """
    Check Space Wrapper
    prevents errors from tanking your turn
    """
    if not check_inbounds(r, c, board_size):
        return False
    try:
        return check_space(r, c)
    except:
        return None

def check_inbounds(r, c, board_size):
    return 0 <= r < board_size and 0 <= c < board_size


def try_move(board_size, team, loc):
    forward = 1 if team == Team.WHITE else -1
    r, c = loc
    r += forward # we want to move forwards
    if check_inbounds(r, c, board_size) and not check_space_w(r, c, board_size): # space empty
        move_forward()
        return True
    return False

"""
wrappers for capture attempts
"""
def try_capture_left(board_size, team, loc):
    return try_capture_h(False, board_size, team, loc)

def try_capture_right(board_size, team, loc):
    return try_capture_h(True, board_size, team, loc)

def try_capture_h(tryRight, board_size, team, loc):
    """
    Try to capture unit at target space
    returns true if capture successful
    false otherwise
    """
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    forward = 1 if team == Team.WHITE else -1
    r, c = loc
    r += forward
    if tryRight:
        c += (forward * -1)
    else:
        c += (forward * 1)
    if check_space_w(r, c, board_size) == opp_team:
        capture(r, c)
        return True
    return False
        
def pawn_turn(board_size, team, loc):
    if try_capture_left(board_size, team, loc): return
    if try_capture_right(board_size, team, loc): return
    if try_move(board_size, team, loc): return


"""
OVERLORD THINGS TO DO
"""

def col_danger(c, board_size, team, board):
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    forward = 1 if team == Team.WHITE else -1
    # don't bother checking spawn row
    loc = 1 if team == team.WHITE else board_size-2
    for dist in range(board_size-1, 0, -1):
        check = check_space_w(loc, c, board_size)
        if check == team:
            return 0
        if check == opp_team:
            return dist
        loc += forward
    return 0

def most_dangerous(danger):
    d = 0
    for i in range(1, len(danger)):
        if danger[i] > danger[d]:
            d = i
    return d

def lord_turn(board_size, team, board):
    spawnrow = 0 if team == Team.WHITE else board_size-1
    danger = [col_danger(c, board_size, team, board) for c in range(0, board_size)]
    dlog("danger arr: " + str(danger))
    loc = most_dangerous(danger)
    # try each row, starting with most pressing and moving rightwards
    for _ in range(board_size):
        if not check_space_w(spawnrow, loc, board_size):
            spawn(spawnrow, loc)
            dlog("spawining at " + str((spawnrow, loc)))
            break
        loc = (loc+1)%board_size
