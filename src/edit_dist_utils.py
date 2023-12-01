'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''
# >> [AF] Don't need to import LIst for the typing, just need list, lowercase
from typing import List


def get_edit_dist_table(row_str: str, col_str: str) -> List[List[int]]:
    # >> [AF] Where'd the docstrings to these methods go? Don't know why you'd nuke
    # them from the skeleton, all methods must have accompanying docstrings! (-2)

    # >> [AF] m, n are poor variable names -- why not indicate their contents, e.g.,
    # row_len, col_len? Much more interpretable (-0.5)
    m, n = len(row_str), len(col_str)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                table[i][j] = j
            elif j == 0:
                table[i][j] = i
            else:
                cost = 0 if row_str[i - 1] == col_str[j - 1] else 1
                table[i][j] = min(
                    table[i - 1][j] + 1,      # Deletion
                    table[i][j - 1] + 1,      # Insertion
                    table[i - 1][j - 1] + cost  # Replacement
                )
                if i > 1 and j > 1 and row_str[i - 1] == col_str[j - 2] and row_str[i - 2] == col_str[j - 1]:
                    # >> [AF] Should not have added cost here (which could have been 0), but rather 1
                    # Replacement is the only transformation that has a chance to add 0
                    table[i][j] = min(table[i][j], table[i - 2][j - 2] + cost)  # Transposition

    return table

def edit_distance(s0: str, s1: str) -> int:
    if s0 == s1:
        return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]

def get_transformation_list(s0: str, s1: str) -> List[str]:
    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))

def get_transformation_list_with_table(s0: str, s1: str, table: List[List[int]]) -> List[str]:
    memo: dict[tuple[int, int], List[str]] = {}

    # >> [AF] Again, should choose better parameter names here, and all methods (helpers or otherwise)
    # should have an accompanying docstring (-1)
    # Also, the method name of "backtrack" isn't great because it doesn't tell you what it does, just
    # how it's doing it
    def backtrack(i: int, j: int) -> List[str]:
        if (i, j) in memo:
            return memo[(i, j)]

        if i == 0:
            result = ["I"] * j
        elif j == 0:
            result = ["D"] * i
        elif s0[i - 1] == s1[j - 1]:
            result = backtrack(i - 1, j - 1)
        else:
            cost = 0 if s0[i - 1] == s1[j - 1] else 1
            replace = ["R"] + backtrack(i - 1, j - 1)
            delete = ["D"] + backtrack(i - 1, j)
            insert = ["I"] + backtrack(i, j - 1)

            if i > 1 and j > 1 and s0[i - 1] == s1[j - 2] and s0[i - 2] == s1[j - 1]:
                transposition = ["T"] + backtrack(i - 2, j - 2)
                # >> [AF] You shouldn't need to compare for minimums here at all since you KNOW
                # that the table's entry at the current row and column IS the minimum (assuming it was
                # completed correctly before being given to this method as an argument); instead, just
                # check if the current cell is the same as one of the candidate sources in the table
                # (making sure to add +1 where appropriate) (-0.5)
                result = min([transposition, replace, delete, insert], key=len)
            else:
                result = min([replace, delete, insert], key=len)

        memo[(i, j)] = result
        return result

    transformations = backtrack(len(s0), len(s1))
    return transformations

# ===================================================
# >>> [AF] Summary
# A great submission that shows strong command of
# programming fundamentals, obviously well tested,
# and a good grasp on the problem and supporting
# theory of edit dist. Indeed, there is definitely
# a lot to like in what you have above, but
# I think you could have linted the style a bit more
# (though I do know there were mitigating circumstances
# surrounding this submission, just commenting for
# posterity). Make sure to pay careful attention to
# *clarity* of your code -- imagine you'll have to sit
# down and understand what it all does years later.
# ---------------------------------------------------
# >>> [AF] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [ ] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [ ] Proper docstrings provided for ALL methods
# [~] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          100 / 100
# -> EditDistUtils:      20 / 20  (-2 / missed test)
# -> DistlePlayer:      272 / 265 (-0.5 / below threshold; max -30)
# Style Penalty:         -4
# Total:                 96 / 100
# ===================================================
