# Day       Time  Rank  Score       Time   Rank  Score
#  21   02:13:34  1882      0   02:14:22    779      0

from functools import cache
from itertools import permutations

import numpy as np

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("21.txt", "r") as f:
        text = f.read()
    codes = text.split("\n")
    positions = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "BAD": (3, 0),
        "0": (3, 1),
        "A": (3, 2),
        "bad": (0, 0),
        "^": (0, 1),
        "a": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }

    directions = {
        "^": (-1, 0),
        "<": (0, -1),
        "v": (1, 0),
        ">": (0, 1),
    }

    for key in positions.keys():
        positions[key] = np.array(positions[key])

    for key in directions.keys():
        directions[key] = np.array(directions[key])

    def all_move_sequences(start, end, avoid):
        # If we don't move, we can just press same button as previous
        if np.array_equal(start, end):
            return ["a"]

        # Calculate the sequence of moves needed
        delta = end - start
        moves = ""
        dr, dc = delta
        moves = ""
        # Go up/down
        moves += "^" * abs(dr) if dr < 0 else "v" * dr
        # Go left/right
        moves += "<" * abs(dc) if dc < 0 else ">" * dc
        valid_seqs = []
        for perm in permutations(moves):
            # Check that this one does not go over the forbidden position
            prev = start
            valid = True
            for move in perm:
                next_pos = prev + directions[move]
                if np.array_equal(next_pos, avoid):
                    valid = False
                    break
                prev = next_pos
            # If it doesn't, we append and add an 'a' that corresponds to actually clicking the button
            if valid:
                valid_seqs.append("".join(perm) + "a")
        return valid_seqs

    @cache
    def min_length(move_seq, limit=2, depth=0):
        # Depth = 0: at numeric keypad
        avoid = positions["BAD"] if depth == 0 else positions["bad"]
        cur_pos = positions["A"] if depth == 0 else positions["a"]
        total_len = 0
        for c in move_seq:
            next_pos = positions[c]
            move_seqs = all_move_sequences(cur_pos, next_pos, avoid)
            # If depth == limit: this is the sequence input to control the very last robot.
            if depth == limit:
                total_len += min(len(seq) for seq in move_seqs)
            # Otherwise, recurse a level up.
            else:
                total_len += min(
                    min_length(move_seq, limit, depth + 1) for move_seq in move_seqs
                )
            cur_pos = next_pos
        return total_len

    for code in codes:
        l1 = min_length(code)
        numeric = int(code[0:3])
        ans1 += l1 * numeric

        l2 = min_length(code, limit=25)
        ans2 += l2 * numeric

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
