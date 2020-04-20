import random

class Patterns:
    """
    Use 's' for self because it won't get checked for that way (is implied)

    formatting for pattern recognition:
    all done from black's perspective (up is forward)
    """
    CHAIN_SHORT_LEFT = [
            str.split(". . . . ."),
            str.split(". O . . ."),
            str.split(". . s . ."),
            str.split(". . . . ."),
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
        predicates = []
        for mat in argv:
            bool_checks = []
            for i in range(RANGE):
                for j in range(RANGE):
                    r = (VIEW_DIST - i)
                    c = (VIEW_DIST - j)
                    if mat[i][j] == ENEMY:
                        bool_checks.append(f"self.check_space(r + ({r}*self.forward), c + ({c}*self.forward)) == self.opp_team")
                    if mat[i][j] == FRIEND:
                        bool_checks.append(f"self.check_space(r + ({r}*self.forward), c + ({c}*self.forward)) == self.team")
                    if mat[i][j] == EMPTY:
                        bool_checks.append(f"self.check_space(r + ({r}*self.forward), c + ({c}*self.forward)) == None")
            predicates.append("(" + " and \\\n    ".join(bool_checks) + ")")
        full_check = " or \\\n    ".join(predicates)
        full_check = full_check.replace(" + (0*self.forward)", "") # drop useless math
        full_check = full_check.replace("(1*self.forward)", "self.forward") # conciseness
        full_check = full_check.replace("c + (-1*self.forward)", "c + self.right") # readability
        full_check = full_check.replace("c + (-2*self.forward)", "c + (2*self.right") # readability
        full_check = full_check.replace("c + self.forward", "c + self.left") # drop useless math
        full_check = full_check.replace("c + (2*self.forward)", "c + (2*self.left") # readability
        function_full = f"def {name}(self):\n    return {full_check}"
        function_full = "    " + function_full.replace("\n", "\n    ") # indent
        return function_full + "\n\n"

gpf = PatternWriter.generate_pattern_function

f = open("DlrmPawn.py", "a")
f.write("\n# New Write, make sure to delete any above writes to avoid duplicate definitions\n")
f.write(gpf("can_move", Patterns.CAN_MOVE))
f.write(gpf("can_capture_left", Patterns.CAP_LEFT))
f.write(gpf("can_capture_right", Patterns.CAP_RIGHT))
f.close()
