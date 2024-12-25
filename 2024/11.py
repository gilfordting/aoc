# Day       Time  Rank  Score       Time   Rank  Score
#  11   00:08:28  1714      0   00:15:45    884      0

import operator
import re
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


deltas = {(-1, 0), (1, 0), (0, 1), (0, -1)}


def process_grid_input(text):
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    def get_neighbors(r, c):
        for dr, dc in deltas:
            next_r, next_c = r + dr, c + dc
            if in_bounds(next_r, next_c):
                return next_r, next_c

    return grid, n_rows, n_cols, in_bounds, get_neighbors


if __name__ == "__main__":
    edges = defaultdict(set)
    with open("11.txt", "r") as f:
        text = f.read()

    stones = list(map(int, text.split()))

    @cache
    def num_stones(start, num_iters):
        if num_iters == 1:
            if start == 0:
                return 1
            if len(str(start)) % 2 == 0:
                return 2
            return 1
        # If more than one remaining
        if start == 0:
            return num_stones(1, num_iters - 1)
        s = str(start)
        if len(s) % 2 == 0:
            x = len(s) // 2
            return num_stones(int(s[:x]), num_iters - 1) + num_stones(
                int(s[x:]), num_iters - 1
            )
        return num_stones(start * 2024, num_iters - 1)

    @cache
    def transform(stone):
        if stone == 0:
            return [1]
        s = str(stone)
        if len(s) % 2 == 0:
            x = len(s) // 2
            s_1, s_2 = int(s[:x]), int(s[x:])
            return [s_1, s_2]
        return [stone * 2024]

    def blink(stones, iteration):
        return sum(
            [transform(stone) for stone in tqdm(stones, desc=f"iteration={iteration}")],
            start=[],
        )

    # for i in tqdm(range(75)):
    #     stones = blink(stones, i)

    # grid, n_rows, n_cols, in_bounds, get_neighbors = process_grid_input(text)

    # for r, row in enumerate(grid):
    #     for c, val in enumerate(row):
    #         if val == 100_000:
    #             pass

    ans = sum(num_stones(i, 75) for i in stones)

    print(ans)
