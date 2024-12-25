# Day       Time  Rank  Score       Time   Rank  Score
#   9   00:37:25  4772      0   01:04:14   2820      0

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


class Node:
    def __init__(self, pos=-1, id_num=None, next_node=None, prev_node=None):
        self.pos = pos
        self.id_num = id_num
        self.next_node = next_node
        self.prev_node = prev_node


def append_chain(id_num, length, prev_node):
    start = Node(prev_node.pos + 1, id_num, prev_node=prev_node)
    prev_node.next_node = start
    curr = start
    for _ in range(length - 1):
        new_node = Node(curr.pos + 1, id_num, prev_node=curr)
        curr.next_node = new_node
        curr = new_node
    return curr  # Very end


def append_empty_chain(length, prev_node):
    return append_chain(None, length, prev_node)


HEAD = Node()
TAIL = None

if __name__ == "__main__":
    edges = defaultdict(set)
    with open("09.txt", "r") as f:
        text = f.read()

    blocks = []
    # Turn it into a linked list?
    id_num = 0
    for i, c in enumerate(text):
        length = int(c)
        if i == 0:
            TAIL = append_chain(id_num, length, HEAD)
            blocks.append((id_num, length))
            id_num += 1
        elif i % 2 == 0:
            TAIL = append_chain(id_num, length, TAIL)
            blocks.append((id_num, length))
            id_num += 1
        else:
            if length == 0:
                continue
            TAIL = append_empty_chain(length, TAIL)
            blocks.append((None, length))

    # curr = HEAD.next_node
    # for _ in range(100):
    #     print(curr.id_num)
    #     curr = curr.next_node

    left, right = HEAD.next_node, TAIL
    checksum = 0
    while left.pos <= right.pos:
        # If left has a valid value, continue
        if left.id_num is not None:
            checksum += left.id_num * left.pos
            left = left.next_node
            continue
        # Otherwise, we need to bring it a proper value
        if right.id_num is not None:
            checksum += right.id_num * left.pos
            left = left.next_node
            right = right.prev_node
            continue
        right = right.prev_node
    print(checksum)
    print(blocks)

    right = len(blocks) - 1
    while right > 0:
        curr_id, curr_length = blocks[right]
        # Don't attempt to move spaces
        if curr_id is None:
            right -= 1
            continue
        index = -1
        # Find the leftmost block of space that fits this
        for i in range(right):
            id, length = blocks[i]
            if id is None and length >= curr_length:
                index = i
                break
        if index == -1:
            right -= 1
            continue
        # Otherwise, we can move it here!
        id, length = blocks[index]
        print(f"Able to move {curr_id} from {right} to {index}")
        blocks[right] = None, curr_length
        if length == curr_length:
            blocks[index] = curr_id, length
            right -= 1
            continue
        # Otherwise we'll need to insert.
        blocks[index] = curr_id, curr_length
        blocks.insert(index + 1, (None, length - curr_length))

    checksum = 0
    pos = 0
    for id, length in blocks:
        if id is None:
            pos += length
            continue
        for _ in range(length):
            checksum += id * pos
            pos += 1
    print(checksum)

    # left, right = 0, len(blocks) - 1
    # while left < right:
    #     id_num_left, length_left = blocks[left]
    #     id_num_right, length_right = blocks[right]
    #     # Wait for a space
    #     if id_num_left is not None:
    #         left += 1
    #         continue
    #     # Fill the space
    #     # If there is empty space on the right, bad
    #     if id_num_right is None:
    #         right -= 1
    #         continue
    #     # Otherwise, attempt to move
    #     # compare length_left and length_right
    #     if length_right > length_left:
    #         # We can't move it
    #         right -= 1
    #         continue
    #     elif length_right == length_left:
    #         # Perfect match
    #         blocks[left] = id_num_right, length_right
    #         blocks[right] = None, length_right
    #     else:
    #         # Inexact match
    #         blocks[left] = id_num_right, length_right
    #         blocks[right] = None, length_right
    #         # Have some space left over
    #         blocks.insert(left + 1, (None, length_left - length_right))
    #         # don't need to decrement right
    #         right -= 1

    # lines = text.split("\n")
    # n_rows, n_cols = len(lines), len(lines[0])

    # def in_bounds(r, c):
    #     return 0 <= r < n_rows and 0 <= c < n_cols

    ans = None
    print(ans)
    # Alternate between length of file and length of free space
