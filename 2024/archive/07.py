# Day       Time  Rank  Score       Time   Rank  Score
#   7   00:11:44  1844      0   00:15:52   1602      0

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
    with open("07.txt", "r") as f:
        text = f.read()
    lines = text.split("\n")
    eqns = []
    for line in lines:
        prefix, ls = line.split(":")
        prefix = int(prefix)
        ls = ls.strip().split(" ")
        ls = list(map(int, ls))
        eqns.append((prefix, ls))

    def possible(target, ls):
        back = ls[-1]
        if len(ls) == 1:
            return back == target
        if target % back == 0 and possible(target // back, ls[:-1]):
            return True
        if target >= back and possible(target - back, ls[:-1]):
            return True
        s_t, s_b = str(target), str(back)
        if len(s_t) >= len(s_b) and s_t[-len(s_b) :] == s_b:
            s = s_t[: -len(s_b)]
            val = 0 if s == "" else int(s)
            if possible(val, ls[:-1]):
                return True
        return False

    print(sum(target for target, ls in tqdm(eqns) if possible(target, ls)))
