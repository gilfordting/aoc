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
from pprint import pprint

import networkx as nx
import numpy as np
from aocd import data, submit
from more_itertools import windowed
from tqdm import tqdm

sys.setrecursionlimit(100_000)

# Helpful constants

LETTERS = {x for x in "abcdefghijklmnopqrstuvwxyz"}
VOWELS = {"a", "e", "i", "o", "u"}
CONSONANTS = LETTERS - VOWELS


# Input processing
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s):
    return lmap(int, re.findall(r"-?\d+", s))


# List functions
def diff(list1, list2=None):
    it = pairwise(list1) if list2 is None else zip(list1, list2)
    return [b - a for a, b in it]


# Grid traversal helpers
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


deltas = {Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)}


class Direction(Enum):
    UP = Point(-1, 0)
    RIGHT = Point(0, 1)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)

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
        return self.value

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

    return grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter


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


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    # # Input type 1: grid
    # grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter = process_grid_input(data)
    # G = nx.grid_graph((n_rows, n_cols))
    # start, end = None, None
    # for r, c, val in grid_iter():
    #     if val == "S":
    #         start = Point(r, c)
    #     elif val == "E":
    #         end = Point(r, c)
    #     elif val == "#":
    #         G.remove_node((r, c))

    # # Dictionary mapping nodes to their distances from start node
    # dist = nx.shortest_path_length(G, start)
    # dist.get(end, float("inf"))

    # # Input type 2: every block is in the same format
    # pattern = r"xxxxxxx"
    # for line in data.split("\n"):
    #     match = re.search(pattern, line)
    #     xxxxxxx = match.groups()

    # # Input type 3: graph
    # vertices = set()
    # edges = defaultdict(set)
    # for line in data.split("\n"):
    #     pass

    for line in data.split("\n"):
        l = ints(line)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")

    # submit(ans1, part="a")
    # submit(ans2, part="b")
