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
next_dir = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

deltas = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


if __name__ == "__main__":
    edges = defaultdict(set)
    with open("08.txt", "r") as f:
        text = f.read()
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    antennae = defaultdict(list)
    used_pos = set()
    for r, line in enumerate(lines):
        for c, chr in enumerate(line):
            if chr == ".":
                continue
            antennae[chr].append((r, c))
            used_pos.add((r, c))

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    def all_locs(loc_a, loc_b):
        r_a, c_a = loc_a
        r_b, c_b = loc_b
        dr = r_b - r_a
        dc = c_b - c_a
        r, c = loc_b
        while in_bounds(r, c):
            r += dr
            c += dc
        # Now step backwards
        r -= dr
        c -= dc
        while in_bounds(r, c):
            yield r, c
            r -= dr
            c -= dc

    antinode_locs = set()
    for ls in tqdm(antennae.values()):
        # print(ls)
        # Look at pairwise locations
        for loc_a, loc_b in combinations(ls, 2):
            # P1
            # r_a, c_a = loc_a
            # r_b, c_b = loc_b
            # dr = r_b - r_a
            # dc = c_b - c_a
            # r_1, c_1 = dr + r_b, dc + c_b
            # r_2, c_2 = r_a - dr, c_a - dc
            # if in_bounds(r_1, c_1):
            #     antinode_locs.add((r_1, c_1))
            # if in_bounds(r_2, c_2):
            #     antinode_locs.add((r_2, c_2))
            # P2
            for r, c in all_locs(loc_a, loc_b):
                antinode_locs.add((r, c))

    ans = len(antinode_locs)
    print(ans)
