

DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

def turn():
    if get_type() == RobotType.PAWN:
        pawn_turn(get_board_size(), get_team(), get_location())
    else:
        lord_turn(get_board_size(), get_team())


"""
PAWN THINGS TO DO
"""

def try_move(team):
    

def pawn_turn(board_size, team, loc):
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

"""
OVERLORD THINGS TO DO
"""

def lord_turn(board_size, team):
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
