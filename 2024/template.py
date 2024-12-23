import heapq
import math
import operator
import re
import sys
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
    islice,
    pairwise,
    permutations,
    zip_longest,
)
from math import prod

import networkx as nx
import numpy as np
from tqdm import tqdm

sys.setrecursionlimit(100_000)


def groupwise(iterable, n=4):
    """
    Create an iterator of overlapping groups of size n from the input iterable.
    Similar to pairwise() but with configurable group size.

    Example:
        groupwise([1,2,3,4,5,6]) -> (1,2,3,4), (2,3,4,5), (3,4,5,6)
    """
    iterator = iter(iterable)
    window = tuple(islice(iterator, n))
    if len(window) == n:
        yield window
    for item in iterator:
        window = window[1:] + (item,)
        yield window


deltas = [np.array((-1, 0)), np.array((0, -1)), np.array((1, 0)), np.array((0, 1))]


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

    @property
    def delta(self):
        return np.array(self.value)

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

    def in_bounds(pos):
        r, c = pos
        return 0 <= r < n_rows and 0 <= c < n_cols

    def get_neighbors(pos):
        for delta in deltas:
            next_pos = pos + delta
            if in_bounds(next_pos):
                yield next_pos

    def grid_iter():
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                yield (r, c), val

    def make_pos(r, c):
        return np.array((r, c))

    return grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter, make_pos


class PriorityQueue:
    def __init__(self):
        self.q = []

    def push(self, item, score):
        heapq.heappush(self.q, (score, item))

    def pop(self):
        score, item = heapq.heappop(self.q)
        return item, score

    def __len__(self):
        return len(self.q)


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
    # Input type 1: grid
    # grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter = process_grid_input(text)
    # G = nx.grid_graph((n_rows, n_cols))
    # start, end = None, None
    # for r, c, val in grid_iter():
    #     if val == "S":
    #         start = make_pos(r, c)
    #     elif val == "E":
    #         end = make_pos(r, c)
    #     elif val == "#":
    #         G.remove_node((r, c))

    # # Dictionary mapping nodes to their distances from start node
    # dist = nx.shortest_path_length(G, start)
    # dist.get(end, float("inf"))

    # Input type 2: every block is in the same format
    # pattern = r"xxxxxxx"
    # for line in text.split("\n"):
    #     match = re.search(pattern, line)
    #     xxxxxxx = match.groups()

    # Input type 3: graph
    # vertices = set()
    # edges = defaultdict(set)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
