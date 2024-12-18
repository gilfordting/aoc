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
    ans = 0
    with open("14.txt", "r") as f:
        text = f.read()
    # Graph input
    # edges = defaultdict(set)
    pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    x_max = 101
    x_mid = (x_max - 1) // 2
    y_max = 103
    y_mid = (y_max - 1) // 2
    totals = [0, 0, 0, 0]

    def get_quadrant(x, y):
        if x < x_mid:
            if y < y_mid:
                return 0
            if y > y_mid:
                return 1
        if x > x_mid:
            if y < y_mid:
                return 2
            if y > y_mid:
                return 3
        return None

    # for line in text.split("\n"):
    #     match = re.search(pattern, line)
    #     p_x, p_y, v_x, v_y = match.groups()
    #     p_x, p_y, v_x, v_y = int(p_x), int(p_y), int(v_x), int(v_y)

    #     def step(p_x, p_y):
    #         return (p_x + v_x) % x_max, (p_y + v_y) % y_max

    #     for _ in range(100):
    #         p_x, p_y = step(p_x, p_y)

    #     # print(p_x, p_y)

    #     quad = get_quadrant(p_x, p_y)
    #     if quad is None:
    #         continue

    #     totals[quad] += 1

    # ans = totals[0] * totals[1] * totals[2] * totals[3]

    positions = []
    velocities = []
    for line in text.split("\n"):
        match = re.search(pattern, line)
        p_x, p_y, v_x, v_y = match.groups()
        p_x, p_y, v_x, v_y = int(p_x), int(p_y), int(v_x), int(v_y)
        positions.append((p_x, p_y))
        velocities.append((v_x, v_y))

    def step_all(positions):
        return [
            ((p_x + v_x) % x_max, (p_y + v_y) % y_max)
            for (p_x, p_y), (v_x, v_y) in zip(positions, velocities)
        ]

    def is_christmas_tree(positions):
        grid = get_grid(positions)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val > 1:
                    return False
        return True

    def get_grid(positions):
        grid = [[0] * x_max for _ in range(y_max)]
        for p_x, p_y in positions:
            grid[p_y][p_x] += 1
        return grid

    def grid_str(positions):
        grid = get_grid(positions)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == 0:
                    grid[r][c] = "."
                else:
                    grid[r][c] = str(grid[r][c])
        s = "\n".join("".join(line) for line in grid)
        return s

    for i in tqdm(range(100_000)):
        if is_christmas_tree(positions):
            ans = i

            with open("14out.txt", "w") as f:
                f.write(grid_str(positions))
            break
        positions = step_all(positions)

    # Grid input
    # grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders = process_grid_input(
    #     text
    # )
    # for r, row in enumerate(grid):
    #     for c, val in enumerate(row):
    #         pass

    print(ans)
