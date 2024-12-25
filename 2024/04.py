# Day       Time  Rank  Score       Time   Rank  Score
#   4   00:30:03  6191      0   00:34:53   4185      0

import re
from collections import Counter
from itertools import pairwise

VALIDS = ("XMAS", "SAMX")

if __name__ == "__main__":
    with open("04.txt", "r") as f:
        text = f.read()
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])

    def num_matches(it):
        return 1 if "".join(it) in VALIDS else 0

    def get_matches_p1(row, col):
        total = 0
        if col + 3 < n_cols:
            total += num_matches(lines[row][col + i] for i in range(4))
        if row + 3 < n_rows:
            total += num_matches(lines[row + i][col] for i in range(4))
        if row + 3 < n_rows and col + 3 < n_cols:
            total += num_matches(lines[row + i][col + i] for i in range(4))
        if row - 3 >= 0 and col + 3 < n_cols:
            total += num_matches(lines[row - i][col + i] for i in range(4))
        return total

    def get_matches_p2(row, col):
        if row + 2 < n_rows and col + 2 < n_cols:
            s1 = "".join(
                [lines[row][col], lines[row + 1][col + 1], lines[row + 2][col + 2]]
            )
            s2 = "".join(
                [lines[row + 2][col], lines[row + 1][col + 1], lines[row][col + 2]]
            )
            if s1 in ("SAM", "MAS") and s2 in ("SAM", "MAS"):
                return 1
        return 0

    print(sum(get_matches_p1(r, c) for r in range(n_rows) for c in range(n_cols)))
    print(sum(get_matches_p2(r, c) for r in range(n_rows) for c in range(n_cols)))
