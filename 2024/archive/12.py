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

    return grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders


if __name__ == "__main__":
    edges = defaultdict(set)
    with open("12.txt", "r") as f:
        text = f.read()

    grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders = process_grid_input(
        text
    )

    visited = set()

    def get_area_perim(r, c):
        val = grid[r][c]
        visited.add((r, c))
        positions = set()
        positions.add((r, c))
        area, perim = 0, 0
        q = [(r, c)]
        while len(q) != 0:
            r, c = q.pop(0)
            area += 1
            perim += num_borders(r, c)
            for next_r, next_c in get_neighbors(r, c):

                next_val = grid[next_r][next_c]
                if next_val == val:
                    if (next_r, next_c) not in visited:
                        visited.add((next_r, next_c))
                        q.append((next_r, next_c))
                        positions.add((next_r, next_c))
                else:
                    perim += 1
        return area, perim, positions

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

    ans = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if (r, c) not in visited:
                area, perim, positions = get_area_perim(r, c)
                sides = get_num_sides(positions, val)
                print(area, perim, val, sides)
                # ans += area * perim
                ans += area * sides

    # ans = None
    print(ans)
