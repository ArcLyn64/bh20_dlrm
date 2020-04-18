import DlrmPawn as dpawn
import DlrmLord as dlord

DEBUG = 1
def dlog(s):
    if DEBUG > 0: log(s)

robot = None
def turn():
    global robot
    if not robot:
        if get_type() == RobotType.PAWN:
            robot = dpawn.Pawn(get_board_size(), get_team())
            dlog("Created Pawn!")
        else:
            robot = dlord.Lord(get_board_size(), get_team())
            dlog("Created Overlord!")
    robot.turn()
