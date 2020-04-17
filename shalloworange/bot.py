import DlrmPawn as dpawn
import DlrmLord as dlord

def turn():
    if get_type() == RobotType.PAWN:
        robot = dpawn.Pawn(get_board_size(), get_team(), get_location())
    else:
        robot = dlord.Lord(get_board_size(), get_team(), get_board())
    robot.turn()
