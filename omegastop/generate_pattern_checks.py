import random

class Patterns:
    """
    Use 's' for self because it won't get checked for that way (is implied)

    formatting for pattern recognition:
    all done from black's perspective (up is forward)
    for mirrors, default is left
    """
    CHAIN_SHORT_LEFT = [
            str.split(". . . . ."),
            str.split(". O . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_SHORT_BACK = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". O . . ."),
            str.split(". . . . .")
            ]

    CHAIN_SHORT_RIGHT = [
            str.split(". . . . ."),
            str.split(". . . O ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_LONG_LEFT = [
            str.split("O . . . ."),
            str.split(". O . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CHAIN_LONG_BACK = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". O . . ."),
            str.split("O . . . .")
            ]

    CHAIN_LONG_RIGHT = [
            str.split(". . . . O"),
            str.split(". . . O ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    SPEAR_TIP = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". O . O ."),
            str.split(". . . . .")
            ]

    CAP_LEFT = [
            str.split(". . . . ."),
            str.split(". X . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CAP_RIGHT = [
            str.split(". . . . ."),
            str.split(". . . X ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    CAN_MOVE = [
            str.split(". . . . ."),
            str.split(". . _ . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    STALEMATE_LEFT = [
            str.split(". X . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    STALEMATE_RIGHT = [
            str.split(". . . X ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    BLOCKED = [
            str.split(". . . . ."),
            str.split(". . X . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    PAIRED_LEFT = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". O s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    PAIRED_RIGHT = [
            str.split(". . . . ."),
            str.split(". . . . ."),
            str.split(". . s O ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    MOVE_TO_DEFEND_RIGHT = [
            str.split(". . . O ."),
            str.split(". . _ . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    MOVE_TO_DEFEND_LEFT = [
            str.split(". O . . ."),
            str.split(". . _ . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]
    
    MOVE_TO_TRADE_CLOSE = [
            str.split(". X . . ."),
            str.split(". . _ . ."),
            str.split(". O s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]
    
    MOVE_TO_TRADE_FAR = [
            str.split(". . . X ."),
            str.split(". . _ . ."),
            str.split(". O s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    ENEMY_FAR = [
            str.split("X . . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]

    ENEMY_CLOSE = [
            str.split(". X . . ."),
            str.split(". . . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
            str.split(". . . . .")
            ]




"""
----------------------------------------------------------
"""
VIEW_DIST = 2
RANGE = 5

class PatternWriter:

    def generate_pattern_function(name, *argv):
        """
        Takes in any number of 5x5 matrix that indicates the total viewspace of the pawn
        X are enemies
        O are friendlies
        _ are empty spaces
        anything else we don't care about
        generates a function which checks if we match any of those patterns
        """
        ENEMY = 'X'
        FRIEND = 'O'
        EMPTY = '_'
        PART1 = "self.check_space(r + ("
        PART2 = "*self.forward), c + ("
        PART3 = "*self.forward))"

        predicates = []
        for mat in argv:
            bool_checks = []
            for i in range(RANGE):
                for j in range(RANGE):
                    r = (VIEW_DIST - i)
                    c = (VIEW_DIST - j)
                    if mat[i][j] == ENEMY:
                        bool_checks.append(PART1 + str(r) + PART2 + str(c) + PART3 + " == self.opp_team")
                    if mat[i][j] == FRIEND:
                        bool_checks.append(PART1 + str(r) + PART2 + str(c) + PART3 + " == self.team")
                    if mat[i][j] == EMPTY:
                        bool_checks.append("not " + PART1 + str(r) + PART2 + str(c) + PART3)
            predicates.append("(" + " and \\\n    ".join(bool_checks) + ")")
        full_check = " or \\\n    ".join(predicates)
        full_check = full_check.replace(" + (0*self.forward)", "") # drop useless math
        full_check = full_check.replace("(1*self.forward)", "self.forward") # conciseness
        full_check = full_check.replace("c + (-1*self.forward)", "c + self.right") # readability
        full_check = full_check.replace("c + (-2*self.forward)", "c + (2*self.right)") # readability
        full_check = full_check.replace("c + self.forward", "c + self.left") # drop useless math
        full_check = full_check.replace("c + (2*self.forward)", "c + (2*self.left)") # readability
        function_full = "def " + name + "(self):\n    r, c = self.loc()\n    return " + full_check
        function_full = "    " + function_full.replace("\n", "\n    ") # indent
        return function_full + "\n\n"

    def generate_pattern_mirror(name, *argv):
        mirrors = [[row[::-1] for row in mat] for mat in argv]
        all_mat = list(argv) + mirrors
        return PatternWriter.generate_pattern_function(name, *all_mat)

def main():
    gpf = PatternWriter.generate_pattern_function
    gpm = PatternWriter.generate_pattern_mirror
    f = open("DlrmPawn.py", "a")
    f.write("\n# New Write, make sure to delete any above writes to avoid duplicate definitions\n")
    f.write(gpf("can_move", Patterns.CAN_MOVE))
    f.write(gpf("can_capture_left", Patterns.CAP_LEFT))
    f.write(gpf("can_capture_right", Patterns.CAP_RIGHT))
    f.write(gpm("move_attacked", Patterns.STALEMATE_LEFT))
    f.write(gpm("move_defended", Patterns.PAIRED_LEFT))
    f.write(gpm("can_move_to_defend", Patterns.MOVE_TO_DEFEND_LEFT))
    f.write(gpm("can_move_to_trade", Patterns.MOVE_TO_TRADE_CLOSE, Patterns.MOVE_TO_TRADE_FAR))
    f.write(gpm("enemy_spotted", Patterns.ENEMY_FAR, Patterns.ENEMY_CLOSE))
    f.write(gpm("short_chain_ahead", Patterns.CHAIN_SHORT_LEFT))
    f.write(gpm("long_chain_ahead", Patterns.CHAIN_LONG_LEFT))
    f.write(gpm("short_chain_behind", Patterns.CHAIN_SHORT_BACK))
    f.write(gpm("long_chain_behind", Patterns.CHAIN_LONG_BACK))
    f.write(gpf("blocked", Patterns.BLOCKED))

    f.close()

main()
