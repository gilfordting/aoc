import math
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
from math import prod

import numpy as np
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

mv_to_dir = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
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


# deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}

delta_corners = {
    ((-1, 0), (0, 1)),
    ((0, 1), (1, 0)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
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

    return grid, n_rows, n_cols, in_bounds, get_neighbors, num_borders


if __name__ == "__main__":
    ans = 0
    with open("15.txt", "r") as f:
        text = f.read()

    # grid_s, moves = text.split("\n\n")
    # # Graph input
    # # edges = defaultdict(set)
    # gridlines = grid_s.split("\n")

    # n_rows, n_cols = len(gridlines) - 2, len(gridlines[0]) - 2
    # grid = [[0] * n_cols for _ in range(n_rows)]

    # robot_r, robot_c = None, None

    # for r, line in enumerate(grid_s.split("\n")[1:-1]):
    #     for c, val in enumerate(line[1:-1]):
    #         grid[r][c] = val
    #         if val == "@":
    #             robot_r, robot_c = r, c

    # def in_bounds(r, c):
    #     return 0 <= r < n_rows and 0 <= c < n_cols

    # # Mutate grid
    # def move(dir, robot_r, robot_c):
    #     assert grid[robot_r][robot_c] == "@"
    #     dr, dc = deltas[dir]
    #     new_r, new_c = robot_r + dr, robot_c + dc
    #     if not in_bounds(new_r, new_c):
    #         return robot_r, robot_c
    #     if grid[new_r][new_c] == "#":
    #         return robot_r, robot_c
    #     # If onto a free space:
    #     if grid[new_r][new_c] == ".":
    #         grid[robot_r][robot_c] = "."
    #         grid[new_r][new_c] = "@"
    #         robot_r, robot_c = new_r, new_c
    #         return robot_r, robot_c

    #     # If there's a box, we need to push it.
    #     # Return True if can move and we did move.
    #     # False if we cannot move and we did not move.
    #     def move_box(r, c, dir):
    #         assert grid[r][c] == "O"
    #         dr, dc = deltas[dir]
    #         new_r, new_c = r + dr, c + dc
    #         if not in_bounds(new_r, new_c):
    #             return False
    #         if grid[new_r][new_c] == "#":
    #             return False
    #         if grid[new_r][new_c] == ".":
    #             grid[new_r][new_c] = "O"
    #             grid[r][c] = "."
    #             return True
    #         if grid[new_r][new_c] == "O":
    #             res = move_box(new_r, new_c, dir)
    #             if res:
    #                 grid[r][c] = "."
    #                 grid[new_r][new_c] = "O"
    #                 return True
    #             else:
    #                 return False

    #     assert grid[new_r][new_c] == "O"
    #     res = move_box(new_r, new_c, dir)
    #     if res:
    #         grid[robot_r][robot_c] = "."
    #         grid[new_r][new_c] = "@"
    #         robot_r, robot_c = new_r, new_c
    #     return robot_r, robot_c

    # def print_grid(grid):
    #     print("\n".join(["".join(c for c in row) for row in grid]))

    # for line in moves.split("\n"):
    #     for c in line:
    #         robot_r, robot_c = move(mv_to_dir[c], robot_r, robot_c)
    #         # print_grid(grid)
    #         # print(robot_r, robot_c)

    # def get_coord(r, c):
    #     return 100 * (r + 1) + c + 1

    # for r, row in enumerate(grid):
    #     for c, val in enumerate(row):
    #         if val == "O":
    #             ans += get_coord(r, c)

    grid_s, moves = text.split("\n\n")
    grid_s = grid_s.replace("#", "##")
    grid_s = grid_s.replace("O", "[]")
    grid_s = grid_s.replace(".", "..")
    grid_s = grid_s.replace("@", "@.")
    # print(grid_s)
    gridlines = grid_s.split("\n")

    n_rows, n_cols = len(gridlines) - 2, len(gridlines[0]) - 4
    grid = [[0] * n_cols for _ in range(n_rows)]

    robot_r, robot_c = None, None

    for r, line in enumerate(grid_s.split("\n")[1:-1]):
        for c, val in enumerate(line[2:-2]):
            grid[r][c] = val
            if val == "@":
                robot_r, robot_c = r, c

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    # r, c are coordinates of the LEFT edge.
    def can_move_box(r, c, dir):
        assert grid[r][c] == "[" and grid[r][c + 1] == "]", f"r = {r} and c = {c}"
        # See if we can move it left or right
        if dir == Direction.RIGHT:
            # look at r, c+2 -- this is where the right edge will be moved to
            if not in_bounds(r, c + 2):
                return False
            if grid[r][c + 2] == "#":
                return False
            if grid[r][c + 2] == ".":
                return True
            if grid[r][c + 2] == "[":
                return can_move_box(r, c + 2, dir)
            assert False
        if dir == Direction.LEFT:
            # look at r, c-1 -- this is where the left edge will be moved to
            if not in_bounds(r, c - 1):
                return False
            if grid[r][c - 1] == "#":
                return False
            if grid[r][c - 1] == ".":
                return True
            if grid[r][c - 1] == "]":
                return can_move_box(r, c - 2, dir)
            assert False
        if dir == Direction.UP:
            # Need to check that both halves can be moved upwards
            # Look at r-1, c and r-1, c+1

            if not in_bounds(r - 1, c):
                return (
                    False  # also implies r-1, c+1 is out of bounds (c+1 always valid)
                )
            # If either side cannot be moved upwards, we cannot move the entire thing
            # If either one is up against a wall:
            if grid[r - 1][c] == "#" or grid[r - 1][c + 1] == "#":
                return False
            if grid[r - 1][c] == "." and grid[r - 1][c + 1] == ".":
                # if both spaces are free, win
                return True
            # here, we know both above are not walls and not both dots.
            # either we have:
            # so, one of them must be a box segment

            # here, cases are:
            # []
            #  X
            #  []
            #  X
            left_no_box = grid[r - 1][c] not in ("[", "]")
            left_moveable = left_no_box or (
                can_move_box(r - 1, c - 1, dir)
                if grid[r - 1][c] == "]"
                else can_move_box(r - 1, c, dir)
            )
            right_no_box = grid[r - 1][c + 1] not in ("[", "]")
            right_moveable = right_no_box or (
                can_move_box(r - 1, c, dir)
                if grid[r - 1][c + 1] == "]"
                else can_move_box(r - 1, c + 1, dir)
            )
            return left_moveable and right_moveable

        # left_no_box = grid[r + 1][c] not in ("[", "]")
        #     left_moveable = left_no_box or (
        #         can_move_box(r + 1, c - 1, dir)
        #         if grid[r + 1][c] == "]"
        #         else can_move_box(r + 1, c, dir)
        #     )
        #     right_no_box = grid[r + 1][c + 1] not in ("[", "]")
        #     right_moveable = right_no_box or (
        #         can_move_box(r + 1, c, dir)
        #         if grid[r + 1][c + 1] == "]"
        #         else can_move_box(r + 1, c + 1, dir)
        #     )
        #     return left_moveable and right_moveable
        if dir == Direction.DOWN:
            if not in_bounds(r + 1, c):
                return False
            if grid[r + 1][c] == "#" or grid[r + 1][c + 1] == "#":
                return False
            if grid[r + 1][c] == "." and grid[r + 1][c + 1] == ".":
                # if both spaces are free, win
                return True
            # here, we know both above are not walls and not both dots.
            # either we have:
            # so, one of them must be a box segment

            # here, cases are:
            # []
            #  X
            #  []
            #  X
            left_no_box = grid[r + 1][c] not in ("[", "]")
            left_moveable = left_no_box or (
                can_move_box(r + 1, c - 1, dir)
                if grid[r + 1][c] == "]"
                else can_move_box(r + 1, c, dir)
            )
            right_no_box = grid[r + 1][c + 1] not in ("[", "]")
            right_moveable = right_no_box or (
                can_move_box(r + 1, c, dir)
                if grid[r + 1][c + 1] == "]"
                else can_move_box(r + 1, c + 1, dir)
            )
            return left_moveable and right_moveable

    # Returns True if box was moved and False otherwise.
    def move_box(r, c, dir):
        print(f"Tried to move box with left edge r = {r} and c = {c}")
        if not can_move_box(r, c, dir):
            return False
        # Everything below should return True
        if dir == Direction.RIGHT:
            # look at r, c+2 -- this is where the right edge will be moved to
            if grid[r][c + 2] == ".":
                grid[r][c] = "."
                grid[r][c + 1] = "["
                grid[r][c + 2] = "]"
                return True
            # Otherwise, a box is in the way!
            move_box(r, c + 2, dir)
            grid[r][c] = "."
            grid[r][c + 1] = "["
            grid[r][c + 2] = "]"
            return True
        if dir == Direction.LEFT:
            # look at r, c-1 -- this is where the left edge will be moved to
            if grid[r][c - 1] == ".":
                grid[r][c - 1] = "["
                grid[r][c] = "]"
                grid[r][c + 1] = "."
                return True
            # Otherwise, a box is in the way!
            move_box(r, c - 2, dir)
            grid[r][c - 1] = "["
            grid[r][c] = "]"
            grid[r][c + 1] = "."
            return True
        if dir == Direction.UP:
            # If the row above has slots taken up by boxes, recursively move those
            # Look at r-1, c and r-1, c+1

            # Single one directly above, bottom two cases not possible
            if grid[r - 1][c] == "[" and grid[r - 1][c + 1] == "]":
                move_box(r - 1, c, dir)
                grid[r - 1][c] = "["
                grid[r - 1][c + 1] = "]"
                grid[r][c] = "."
                grid[r][c + 1] = "."
                return True

            # Move the one occupying the upper left edge, if it exists
            if grid[r - 1][c] == "]":
                move_box(r - 1, c - 1, dir)

            # Move the one occupying the upper right edge, if it exists
            if grid[r - 1][c + 1] == "[":
                move_box(r - 1, c + 1, dir)

            # Lastly, move the current box up
            grid[r - 1][c] = "["
            grid[r - 1][c + 1] = "]"
            grid[r][c] = "."
            grid[r][c + 1] = "."
            return True
        if dir == Direction.DOWN:
            # If the row above has slots taken up by boxes, recursively move those
            # Look at r-1, c and r-1, c+1

            # Single one directly above, bottom two cases not possible
            if grid[r + 1][c] == "[" and grid[r + 1][c + 1] == "]":
                move_box(r + 1, c, dir)
                grid[r + 1][c] = "["
                grid[r + 1][c + 1] = "]"
                grid[r][c] = "."
                grid[r][c + 1] = "."
                return True

            # Move the one occupying the upper left edge, if it exists
            if grid[r + 1][c] == "]":
                move_box(r + 1, c - 1, dir)

            # Move the one occupying the upper right edge, if it exists
            if grid[r + 1][c + 1] == "[":
                move_box(r + 1, c + 1, dir)

            # Lastly, move the current box up
            grid[r + 1][c] = "["
            grid[r + 1][c + 1] = "]"
            grid[r][c] = "."
            grid[r][c + 1] = "."
            return True

    # Mutate grid
    def move(dir, robot_r, robot_c):
        dr, dc = deltas[dir]
        next_r, next_c = robot_r + dr, robot_c + dc
        if not in_bounds(next_r, next_c):
            return robot_r, robot_c
        if grid[next_r][next_c] == "#":
            return robot_r, robot_c
        if grid[next_r][next_c] == ".":
            grid[next_r][next_c] = "@"
            grid[robot_r][robot_c] = "."
            return next_r, next_c
        # If we encounter a box??
        if grid[next_r][next_c] == "[":
            success = move_box(next_r, next_c, dir)
            if success:
                grid[next_r][next_c] = "@"
                grid[robot_r][robot_c] = "."
                return next_r, next_c
            else:
                return robot_r, robot_c
        if grid[next_r][next_c] == "]":
            success = move_box(next_r, next_c - 1, dir)
            if success:
                grid[next_r][next_c] = "@"
                grid[robot_r][robot_c] = "."
                return next_r, next_c
            else:
                return robot_r, robot_c

    def print_grid(grid):
        print("\n".join(["".join(c for c in row) for row in grid]))

    i = 0
    for line in moves.split("\n"):
        for c in line:
            dir = mv_to_dir[c]
            # print(f"Iteration {i}: moving in direction {dir}")
            robot_r, robot_c = move(dir, robot_r, robot_c)
            # print(f"Robot ends up at {robot_r}, {robot_c}")
            # print_grid(grid)
            i += 1

    # Sum over all GPS coords

    def get_coord(r, c):
        return 100 * (r + 1) + c + 2

    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "[":
                ans += get_coord(r, c)

    print(ans)
