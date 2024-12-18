import heapq
import math
import multiprocessing
import operator
import re
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
    repeat,
    zip_longest,
)
from math import prod

import numpy as np
from tqdm import tqdm

deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}


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


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


# Direction-based
chr_to_dir = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
}

dir_deltas = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


next_dir_cw = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

next_dir_ccw = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
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


class Program:
    def __init__(self, a, b, c, insts):
        self.ip = 0
        self.a = a
        self.b = b
        self.c = c
        self.insts = insts

    def combo_to_val(self, operand):
        if operand < 4:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        assert False, f"got {operand} as an operand"

    def adv(self, operand):
        num = self.a
        denom = 2 ** self.combo_to_val(operand)
        self.a = math.trunc(num / denom)
        self.ip += 2
        return None

    def bxl(self, operand):
        self.b = self.b ^ operand
        self.ip += 2
        return None

    def bst(self, operand):
        val = self.combo_to_val(operand)
        self.b = val % 8
        self.ip += 2
        return None

    def jnz(self, operand):
        if self.a == 0:
            self.ip += 2
            return None
        self.ip = operand
        return None

    def bxc(self, operand):
        self.b = self.b ^ self.c
        self.ip += 2
        return None

    def out(self, operand):
        val = self.combo_to_val(operand)
        self.ip += 2
        return val % 8

    def bdv(self, operand):
        num = self.a
        denom = 2 ** self.combo_to_val(operand)
        self.b = math.trunc(num / denom)
        self.ip += 2
        return None

    def cdv(self, operand):
        num = self.a
        denom = 2 ** self.combo_to_val(operand)
        self.c = math.trunc(num / denom)
        self.ip += 2
        return None

    def run_op(self, opcode, operand):
        mapping = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        return mapping[opcode](operand)

    def run_program(self):
        outputs = []
        while self.ip < len(self.insts):
            opcode, operand = self.insts[self.ip], self.insts[self.ip + 1]
            res = self.run_op(opcode, operand)
            if res is not None:
                outputs.append(res)
        return ",".join(str(i) for i in outputs)


def task(inp):
    i, insts_str = inp
    a, b, c = i, 0, 0
    insts = [int(c) for c in insts_str.split(",")]
    prog = Program(a, b, c, insts)
    outputs = prog.run_program()
    return outputs == insts_str


if __name__ == "__main__":
    with open("17.txt", "r") as f:
        text = f.read()
    # "Every block is in the same format" input
    pattern = (
        r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([,\d]+)"
    )
    match = re.search(pattern, text)
    a, b, c, insts_str = match.groups()
    a, b, c = int(a), int(b), int(c)

    # Part 1: just run the program
    insts = [int(i) for i in insts_str.split(",")]
    prog = Program(a, b, c, insts)
    outputs = prog.run_program()
    print(outputs)

    # Part 2: reverse-engineer the program
    a_vals = [0]  # We know on the last iteration, there was no jump. So a must be 0
    for i in range(len(insts)):
        print(f"Solving for iteration -{i+1}")
        next_a_vals = []
        for a in a_vals:
            print(f"testing a // 8 = {a}")
            for j in range(8):
                a_poss = a * 8 + j
                prog = Program(a_poss, 0, 0, insts)
                output = prog.run_program()
                if insts_str.endswith(output):
                    print(f"a % 8 = {j} worked!")
                    next_a_vals.append(a * 8 + j)
                    print(f"next iteration, try {a * 8 + j}")
        a_vals = next_a_vals

    print(min(a_vals))
