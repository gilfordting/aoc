import heapq
import math
import operator
import re
from bisect import bisect_left
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

import networkx as nx
import numpy as np
from tqdm import tqdm


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


deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    # Clockwise rotation
    @property
    def next(self):
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }[self]

    # Counterclockwise rotation
    @property
    def prev(self):
        return {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
        }[self]

    # Called when the initialization value is not a tuple. This way, we can do Direction('^')
    @classmethod
    def _missing_(cls, value):
        return {
            "^": cls.UP,
            "v": cls.DOWN,
            "<": cls.LEFT,
            ">": cls.RIGHT,
        }[value]


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

    def grid_iter():
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                yield r, c, val

    return grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter


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


# if find first: pattern is like 0 0 0 0 0 0 1 1 1 1 1. returns the index of the first 1
# if find last: pattern is like 1 1 1 1 1 0 0 0. returns index of the last 1
def binary_search_answer(lower_bound, upper_bound, check, find_first=True):
    if find_first:
        return (
            bisect_left(range(lower_bound, upper_bound + 1), True, key=check)
            + lower_bound
        )
    # Invert so we can use the same logic as find_first. Here, we want the index of the last 0 (before the first 1)
    not_check = lambda x: not check(x)
    return (
        bisect_left(range(lower_bound, upper_bound + 1), True, key=not_check)
        + lower_bound
        - 1
    )


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("XXXXXX.txt", "r") as f:
        text = f.read()
    # Graph input
    # edges = defaultdict(set)

    # Grid input
    # grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter = (
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

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
