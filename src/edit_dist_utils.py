'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''
from typing import List


def get_edit_dist_table(row_str: str, col_str: str) -> List[List[int]]:
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
                result = min([transposition, replace, delete, insert], key=len)
            else:
                result = min([replace, delete, insert], key=len)

        memo[(i, j)] = result
        return result

    transformations = backtrack(len(s0), len(s1))
    return transformations