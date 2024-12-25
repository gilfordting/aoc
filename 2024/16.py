# Day       Time  Rank  Score       Time   Rank  Score
#  16   00:37:37  2606      0   20:17:31  17148      0

import heapq
import math
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
from math import prod

import numpy as np
from tqdm import tqdm

sys.setrecursionlimit(100_000_000)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
# 90 degree rotations
next_dir_clockwise = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

next_dir_counterclockwise = {
    Direction.UP: Direction.LEFT,
    Direction.RIGHT: Direction.UP,
    Direction.DOWN: Direction.RIGHT,
    Direction.LEFT: Direction.DOWN,
}

deltas = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


class Node:
    def __init__(self, pos=-1, id_num=None, next_node=None, prev_node=None):
        self.pos = pos
        self.id_num = id_num
        self.next_node = next_node
        self.prev_node = prev_node


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


# deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}

# delta_corners = {
#     ((-1, 0), (0, 1)),
#     ((0, 1), (1, 0)),
#     ((1, 0), (0, -1)),
#     ((0, -1), (-1, 0)),
# }


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

    return grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders


if __name__ == "__main__":
    ans = float("inf")
    with open("16.txt", "r") as f:
        text = f.read()
    # Graph input
    # edges = defaultdict(set)

    # Grid input
    grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders = process_grid_input(
        text
    )

    # "Every block is in the same format" input
    # pattern = r"xxxxxxx"
    # for line in text.split("\n"):
    #     match = re.search(pattern, line)
    #     xxxxxxx = match.groups()

    # Processing the input
    start = None
    end = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "E":
                assert end is None
                end = (r, c)
            elif val == "S":
                assert start is None
                start = (r, c)

    # Try Dijkstra's instead
    q = PriorityQueue()
    traces = {}  # Maps state to pair of best score, and set of all nodes preceding it
    start_state = (start, Direction.RIGHT)
    q.push(start_state, 0)
    traces[start_state] = (0, [])
    while len(q) != 0:
        score, state = q.pop()
        assert state in traces
        pos, dir = state
        r, c = pos
        assert grid[r][c] != "#"
        if pos == end:
            continue  # Don't break because there might be multiple ways of getting here. Later we'll iterate over all possible directions with pos == end
        # If we reach a next_state that is already in traces, we can simply append to parents if our score is the same

        # 1. Continue in same direction
        dr, dc = deltas[dir]
        next_r, next_c = r + dr, c + dc
        # Check that it's valid first
        next_state = ((next_r, next_c), dir)
        next_score = score + 1
        if in_bounds(next_r, next_c) and grid[next_r][next_c] != "#":
            if next_state not in traces:
                traces[next_state] = (next_score, [state])
                q.push(next_state, next_score)
            else:
                prev_best_score, prev_parents = traces[next_state]
                if next_score == prev_best_score:
                    prev_parents.append(state)
                # elif next_score < prev_best_score:
                #     # Have to redo starting from here!
                #     scores[next_state] = (next_score, [state])
                #     q.append(next_state)

        # 2. Turn 90 degrees clockwise
        next_dir = next_dir_clockwise[dir]
        next_state = (pos, next_dir)
        next_score = score + 1000
        if next_state not in traces:
            traces[next_state] = (next_score, [state])
            q.push(next_state, next_score)
        else:
            prev_best_score, prev_parents = traces[next_state]
            if next_score == prev_best_score:
                prev_parents.append(state)

        # 3. Turn 90 degrees counterclockwise
        next_dir = next_dir_counterclockwise[dir]
        next_state = (pos, next_dir)
        next_score = score + 1000
        if next_state not in traces:
            traces[next_state] = (next_score, [state])
            q.push(next_state, next_score)
        else:
            prev_best_score, prev_parents = traces[next_state]
            if next_score == prev_best_score:
                prev_parents.append(state)

    print(start)
    print(end)
    poss_end_states = [(end, dir) for dir in all_directions if (end, dir) in traces]
    min_score = min(traces[(pos, dir)][0] for (pos, dir) in poss_end_states)
    states = [
        (pos, dir)
        for (pos, dir) in poss_end_states
        if traces[(pos, dir)][0] == min_score
    ]
    marked_squares = set()
    while len(states) != 0:
        next_states = []
        for state in states:
            pos, dir = state
            marked_squares.add(pos)
            _, parents = traces[state]
            for s in parents:
                next_states.append(s)
        states = next_states
    print(f"p1_ans={min_score}")
    print(f"p2_ans={len(marked_squares)}")
