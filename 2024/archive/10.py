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

if __name__ == "__main__":
    edges = defaultdict(set)
    with open("10.txt", "r") as f:
        text = f.read()

    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    grid = []
    for line in lines:
        grid.append([int(height) for height in line])

    start_points = set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                start_points.add((r, c))

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    def get_score(r, c):
        score = 0
        start = (r, c)
        # visited = set()
        # visited.add(start)
        q = [start]
        reachable = set()
        while len(q) != 0:
            r, c = q.pop(0)
            val = grid[r][c]
            if val == 9:
                reachable.add((r, c))
                score += 1
                continue
            for dr, dc in deltas:
                new_r, new_c = r + dr, c + dc
                if not in_bounds(new_r, new_c):
                    continue
                if grid[new_r][new_c] == val + 1:
                    q.append((new_r, new_c))
        return score
        return len(reachable)

    print(start_points)
    # scores = get_score(0, 2)
    scores = sum(get_score(r, c) for r, c in start_points)
    print(scores)

    ans = None
    print(ans)
