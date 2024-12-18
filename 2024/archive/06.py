# Day       Time  Rank  Score       Time   Rank  Score
#   6   00:23:03  4321      0   00:41:14   2593      0

import operator
import re
from collections import Counter, defaultdict
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


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


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


def copy_grid(grid):
    return [l[:] for l in grid]


def main():
    edges = defaultdict(set)
    with open("06.txt", "r") as f:
        text = f.read()
    lines = text.split("\n")
    grid = []
    n_rows = len(lines)
    n_cols = len(lines[0])
    guard_r = None
    guard_c = None
    guard_char = None
    for i, line in enumerate(lines):
        chars = [s for s in line]
        grid.append(chars)
        for c in ("^", "<", ">", "v"):
            if c in chars:
                print(f"found {c}")
                guard_r = i
                guard_c = chars.index(c)
                guard_char = c
    guard_state = {
        "^": Direction.UP,
        "v": Direction.DOWN,
        "<": Direction.LEFT,
        ">": Direction.RIGHT,
    }[guard_char]
    grid[guard_r][guard_c] = "X"
    num_visited = 1

    true_grid = copy_grid(grid)
    start_r, start_c = guard_r, guard_c
    start_state = guard_state

    def step():  # returns True if done
        nonlocal guard_state, guard_r, guard_c, num_visited

        if guard_state == Direction.UP:
            # Go all the way up
            last_r = guard_r
            for r in range(guard_r - 1, -1, -1):
                grid_char = grid[r][guard_c]
                # stop here
                if grid_char == "#":
                    break
                # visited already
                elif grid_char == "X":
                    last_r = r
                    continue
                # not visited
                elif grid_char == ".":
                    # Visit this space
                    grid[r][guard_c] = "X"
                    num_visited += 1
                    last_r = r
            guard_r = last_r
            guard_state = next_dir[guard_state]
            # If we left the grid, return True
            if guard_r == 0 and grid[guard_r][guard_c] == "X":
                return True
        elif guard_state == Direction.DOWN:
            # Go all the way down
            last_r = guard_r
            for r in range(guard_r + 1, n_rows):
                grid_char = grid[r][guard_c]
                # stop here
                if grid_char == "#":
                    break
                # visited already
                elif grid_char == "X":
                    last_r = r
                    continue
                # not visited
                elif grid_char == ".":
                    # Visit this space
                    grid[r][guard_c] = "X"
                    num_visited += 1
                    last_r = r
            guard_r = last_r
            guard_state = next_dir[guard_state]
            # If we left the grid, return True
            if guard_r == n_rows - 1 and grid[guard_r][guard_c] == "X":
                return True
        elif guard_state == Direction.LEFT:
            # Go all the way down
            last_c = guard_c
            for c in range(guard_c - 1, -1, -1):
                grid_char = grid[guard_r][c]
                # stop here
                if grid_char == "#":
                    break
                # visited already
                elif grid_char == "X":
                    last_c = c
                    continue
                # not visited
                elif grid_char == ".":
                    # Visit this space
                    grid[guard_r][c] = "X"
                    num_visited += 1
                    last_c = c
            guard_c = last_c
            guard_state = next_dir[guard_state]
            # If we left the grid, return True
            if guard_c == 0 and grid[guard_r][guard_c] == "X":
                return True
        else:
            # Go all the way down
            last_c = guard_c
            for c in range(guard_c + 1, n_cols):
                grid_char = grid[guard_r][c]
                # stop here
                if grid_char == "#":
                    break
                # visited already
                elif grid_char == "X":
                    last_c = c
                    continue
                # not visited
                elif grid_char == ".":
                    # Visit this space
                    grid[guard_r][c] = "X"
                    num_visited += 1
                    last_c = c
            guard_c = last_c
            guard_state = next_dir[guard_state]
            # If we left the grid, return True
            if guard_c == n_cols - 1 and grid[guard_r][guard_c] == "X":
                return True
        return False

    # step()
    while True:
        res = step()
        print(res)
        print("\n".join("".join(line) for line in grid))
        print(num_visited)
        if res:
            break

    # Get all the positions on the grid where the guard would patrol
    positions = set()
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == "X" and (r, c) != (start_r, start_c):
                positions.add((r, c))

    def causes_loop(r, c):
        grid = copy_grid(true_grid)
        grid[r][c] = "#"
        guard_r, guard_c = start_r, start_c
        guard_state = start_state
        visited = set()
        # Keep going
        off_board = False
        while (guard_r, guard_c, guard_state) not in visited:
            visited.add((guard_r, guard_c, guard_state))
            # Attempt to move -- we might get onto a "#", or we might go off the board
            dr, dc = deltas[guard_state]
            guard_r += dr
            guard_c += dc
            # Check if we went off the board
            if guard_r < 0 or guard_r >= n_rows or guard_c < 0 or guard_c >= n_cols:
                off_board = True
                break
            # Check if we hit an obstacle
            while grid[guard_r][guard_c] == "#":
                # Backtrack
                guard_r -= dr
                guard_c -= dc
                # Try again
                guard_state = next_dir[guard_state]
                dr, dc = deltas[guard_state]
                guard_r += dr
                guard_c += dc
        return not off_board

    total = 0
    for r, c in positions:
        if causes_loop(r, c):
            total += 1
    print(causes_loop(8, 6))
    print(total)


if __name__ == "__main__":
    main()
