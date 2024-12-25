# Day       Time  Rank  Score       Time   Rank  Score
#   3   00:22:56  9012      0   00:27:17   5406      0

import re
from collections import Counter
from itertools import pairwise

if __name__ == "__main__":
    with open("03.txt", "r") as f:
        text = f.read()
    # pattern = r"mul\((\d+),(\d+)\)"
    # matches = re.finditer(pattern, text)
    # total = 0
    # for match in matches:
    #     a, b = int(match.group(1)), int(match.group(2))
    #     total += a * b
    # print(total)
    pattern = r"(mul\((\d+),(\d+)\))|do\(\)|don\'t\(\)"
    matches = re.finditer(pattern, text)
    enabled = True
    total = 0
    for match in matches:
        s = match.group()
        if s == "do()":
            enabled = True
        elif s == "don't()":
            enabled = False
        elif enabled:
            a, b = int(match.group(2)), int(match.group(3))
            total += a * b
    print(total)
