# Day       Time  Rank  Score       Time   Rank  Score
#  13   00:13:03   988      0   00:56:10   2574      0

import operator
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from enum import Enum
from functools import cache, reduce
from graphlib import TopologicalSorter
from itertools import (
    accumulate,
    combinations,
    groupby,
    pairwise,
    permutations,
    zip_longest,
)

import numpy as np

sys.setrecursionlimit(500_000_000)

from tqdm import tqdm


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# 90 degree rotations
# next_dir = {
#     Direction.UP: Direction.RIGHT,
#     Direction.RIGHT: Direction.DOWN,
#     Direction.DOWN: Direction.LEFT,
#     Direction.LEFT: Direction.UP,
# }

# deltas = {
#     Direction.UP: (-1, 0),
#     Direction.DOWN: (1, 0),
#     Direction.LEFT: (0, -1),
#     Direction.RIGHT: (0, 1),
# }


class Node:
    def __init__(self, pos=-1, id_num=None, next_node=None, prev_node=None):
        self.pos = pos
        self.id_num = id_num
        self.next_node = next_node
        self.prev_node = prev_node


deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}

delta_corners = {
    ((-1, 0), (0, 1)),
    ((0, 1), (1, 0)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
}


def process_grid_input(text):
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    grid = []
    for line in lines:
        grid.append([c for c in line])

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    def get_neighbors(r, c):
        for dr, dc in deltas:
            next_r, next_c = r + dr, c + dc
            if in_bounds(next_r, next_c):
                yield next_r, next_c

    def num_borders(r, c):
        horiz = 1 if r in (0, n_rows - 1) else 0
        vert = 1 if c in (0, n_cols - 1) else 0
        return horiz + vert

    def get_num_sides(positions, val):
        # can we count the number of corners instead?
        corners = 0
        for r, c in positions:

            for (dr1, dc1), (dr2, dc2) in delta_corners:
                # this counts outwards facing corners
                if not in_bounds(r + dr1, c + dc1) or grid[r + dr1][c + dc1] != val:
                    if not in_bounds(r + dr2, c + dc2) or grid[r + dr2][c + dc2] != val:
                        corners += 1
                print(r, c, dr1, dc1, dr2, dc2)
                if in_bounds(r + dr1, c + dc1) and grid[r + dr1][c + dc1] == val:
                    if in_bounds(r + dr2, c + dc2) and grid[r + dr2][c + dc2] == val:
                        print(r + dr1 + dr2, c + dc1 + dc2)
                        if grid[r + dr1 + dr2][c + dc1 + dc2] != val:
                            corners += 1
        return corners

    return grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders, get_num_sides


if __name__ == "__main__":
    # Setting up
    ans = 0
    with open("13.txt", "r") as f:
        text = f.read()
    # Graph input
    # edges = defaultdict(set)
    # # Grid input
    # grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders, get_num_sides = (
    #     process_grid_input(text)
    # )
    queries = text.split("\n\n")
    print(queries)
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"

    def get_tokens(button_a, button_b, prize):
        a_x, a_y = button_a
        b_x, b_y = button_b
        prize_x, prize_y = prize

        # max_num_a_presses = min(prize_x // a_x, prize_y // a_y)
        # max_num_b_presses = min(prize_x // b_x, prize_y // b_y)

        # def num_tokens_for(num_a_presses, num_b_presses):
        #     if (
        #         prize_x == num_a_presses * a_x + num_b_presses * b_x
        #         and prize_y == num_a_presses * a_y + num_b_presses * b_y
        #     ):
        #         return 3 * num_a_presses + num_b_presses
        #     return float("inf")

        # return min(
        #     num_tokens_for(a_p, b_p)
        #     for a_p in tqdm(range(max_num_a_presses + 1))
        #     for b_p in range(max_num_b_presses + 1)
        # )
        det = a_x * b_y - b_x * a_y
        ans_1 = prize_x * b_y - prize_y * b_x
        ans_2 = -prize_x * a_y + prize_y * a_x
        if ans_1 % det == 0 and ans_2 % det == 0:
            ans_1 //= det
            ans_2 //= det
            if ans_1 >= 0 and ans_2 >= 0:
                return 3 * ans_1 + ans_2
        return None

        # visited = set()
        # q = [(0, 0, 0)]
        # visited.add((0, 0, 0))
        # options = set()
        # while len(q) != 0:
        #     # print(q)
        #     p_x, p_y, curr_tokens = q.pop(0)
        #     if p_x == prize_x and p_y == prize_y:
        #         options.add(curr_tokens)
        #         continue
        #     # Try a
        #     optiona_x, optiona_y, tokens_a = p_x + a_x, p_y + a_y, curr_tokens + 3
        #     optionb_x, optionb_y, tokens_b = p_x + b_x, p_y + b_y, curr_tokens + 1
        #     # Don't add invalid ones
        #     if optiona_x <= prize_x and optiona_y <= prize_y:
        #         q.append((optiona_x, optiona_y, tokens_a))
        #         visited.add((optiona_x, optiona_y, tokens_a))
        #     if optionb_x <= prize_x and optionb_y <= prize_y:
        #         q.append((optionb_x, optionb_y, tokens_b))
        #         visited.add((optionb_x, optionb_y, tokens_b))

        # @cache
        # def num_tokens(curr_x, curr_y):
        #     if curr_x > prize_x or curr_y > prize_y:
        #         return None
        #     if curr_x == prize_x and curr_y == prize_y:
        #         return 0
        #     choice_a = num_tokens(curr_x + a_x, curr_y + a_y)
        #     choice_b = num_tokens(curr_x + b_x, curr_y + b_y)
        #     if choice_a is None and choice_b is None:
        #         return None
        #     if choice_a is None:
        #         return choice_b + 1
        #     if choice_b is None:
        #         return choice_a + 3
        #     return min(choice_b + 1, choice_a + 3)

        # return num_tokens(0, 0)

        # @cache
        # def num_tokens(prize_x, prize_y):
        #     if prize_x < 0 or prize_y < 0:
        #         return None
        #     # if curr_x > prize_x or curr_y > prize_y:
        #     #     return None
        #     if prize_x == 0 and prize_y == 0:
        #         return 0
        #     # if curr_x == prize_x and curr_y == prize_y:
        #     #     return 0
        #     choice_a = num_tokens(prize_x - a_x, prize_y - a_y)
        #     choice_b = num_tokens(prize_x - b_x, prize_y - b_y)
        #     if choice_a is None and choice_b is None:
        #         return None
        #     if choice_a is None:
        #         return choice_b + 1
        #     if choice_b is None:
        #         return choice_a + 3
        #     return min(choice_b + 1, choice_a + 3)

        # commons = ()

        # # We need to figure out common_x and common_y
        # def find_commons(curr_x, curr_y, n_tokens):
        #     print(curr_x, curr_y, n_tokens)
        #     if curr_x != 0 and curr_x == curr_y:
        #         commons.add((curr_x, curr_y, n_tokens))
        #         return
        #     find_commons(curr_x + a_x, curr_y + a_y, n_tokens + 3)
        #     find_commons(curr_x + b_x, curr_y + b_y, n_tokens + 1)

        # find_commons(0, 0, 0)

        # DP?
        # dp = [[float("inf")] * (prize_y + 1) for _ in range(prize_x + 1)]
        # dp[0][0] = 0
        # for x in range(prize_x + 1):
        #     for y in range(prize_y + 1):
        #         option_a = (
        #             dp[x - a_x][y - a_y] if x >= a_x and y >= a_y else float("inf")
        #         )
        #         option_b = (
        #             dp[x - b_x][y - b_y] if x >= b_x and y >= b_y else float("inf")
        #         )
        #         dp[x][y] = min(option_a, option_b)

        # return dp[prize_x][prize_y]

        # return num_tokens(prize_x, prize_y)

    for query in tqdm(queries):
        match = re.search(pattern, query)
        button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y = (
            match.groups()
        )
        data = {
            "button_a": (int(button_a_x), int(button_a_y)),
            "button_b": (int(button_b_x), int(button_b_y)),
            "prize": (int(prize_x), int(prize_y)),
        }
        data["prize"] = 10000000000000 + int(prize_x), 10000000000000 + int(prize_y)
        # Part 1
        tokens = get_tokens(data["button_a"], data["button_b"], data["prize"])
        if tokens is not None:
            ans += tokens

    # for r, row in enumerate(grid):
    #     for c, val in enumerate(row):
    #         pass

    print(ans)
