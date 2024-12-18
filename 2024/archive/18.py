import heapq
import math
import operator
import re
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
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
from math import prod

import numpy as np
from tqdm import tqdm

deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}


class PriorityQueue:
    def __init__(self):
        self.q = []

    def push(self, item, score):
        heapq.heappush(self.q, (score, item))

    def pop(self):
        score, item = heapq.heappop(self.q)
        return score, item

    def __len__(self):
        return len(self.q)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


# Direction-based
chr_to_dir = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
}

dir_deltas = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


next_dir_cw = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

next_dir_ccw = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
}


def process_grid_input(text):
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    grid = [[c for c in line] for line in lines]

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

    def grid_iter():
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                yield r, c, val

    return grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders, grid_iter


if __name__ == "__main__":
    ans = 0
    with open("18.txt", "r") as f:
        text = f.read()
    n_rows, n_cols = 71, 71
    byte_positions = []
    for line in text.split("\n"):
        c, r = line.split(",")
        c, r = int(c), int(r)
        byte_positions.append((r, c))

    grid = [[True] * n_cols for _ in range(n_rows)]
    for i in range(1024):
        r, c = byte_positions[i]
        grid[r][c] = False

    q = [(0, 0)]
    dist = {(0, 0): 0}

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    while len(q) != 0:
        pos = q.pop(0)
        r, c = pos
        assert pos in dist
        assert grid[r][c]
        if pos == (70, 70):
            ans = dist[pos]
            break
        for dr, dc in deltas:
            new_r, new_c = r + dr, c + dc
            if (
                in_bounds(new_r, new_c)
                and grid[new_r][new_c]
                and (new_r, new_c) not in dist
            ):
                q.append((new_r, new_c))
                dist[(new_r, new_c)] = dist[pos] + 1

    print(ans)

    # Part 2
    grid = [[True] * n_cols for _ in range(n_rows)]

    def is_separated(grid):
        q = [(0, 0)]
        visited = set()
        visited.add((0, 0))

        while len(q) != 0:
            pos = q.pop(0)
            r, c = pos
            assert pos in visited
            assert grid[r][c]
            if pos == (70, 70):
                return False
            for dr, dc in deltas:
                new_r, new_c = r + dr, c + dc
                if (
                    in_bounds(new_r, new_c)
                    and grid[new_r][new_c]
                    and (new_r, new_c) not in visited
                ):
                    q.append((new_r, new_c))
                    visited.add((new_r, new_c))
        return True

    # can do binary search, but had finished by the time i had started it and started writing binary search :p
    for r, c in tqdm(byte_positions):
        grid[r][c] = False
        if is_separated(grid):
            print(f"{c},{r}")
            break
