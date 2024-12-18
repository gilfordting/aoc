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


def bfs(start_state, get_neighbors, stop_condition):
    q = [start_state]
    visited = set(q)
    while len(q) != 0:
        state = q.pop(0)
        assert state in visited
        if stop_condition(state):
            pass  # do custom logic here
        for next_state in get_neighbors(state):
            q.append(next_state)
            visited.add(next_state)


if __name__ == "__main__":
    ans = 0
    with open("XXXXXX.txt", "r") as f:
        text = f.read()
    # Graph input
    # edges = defaultdict(set)

    # Grid input
    # grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders, grid_iter = (
    #     process_grid_input(text)
    # )

    # "Every block is in the same format" input
    # pattern = r"xxxxxxx"
    # for line in text.split("\n"):
    #     match = re.search(pattern, line)
    #     xxxxxxx = match.groups()

    # Processing the input
    # for r, c, val in grid_iter():
    #     pass

    print(ans)
