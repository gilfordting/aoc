# Day       Time  Rank  Score       Time   Rank  Score
#  25   00:08:02   440      0   00:08:11    382      0

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("25.txt", "r") as f:
        text = f.read()

    def is_lock(grid):
        lines = grid.split("\n")
        return lines[0] == "#" * 5 and lines[-1] == "." * 5

    def is_key(grid):
        lines = grid.split("\n")
        return lines[0] == "." * 5 and lines[-1] == "#" * 5

    def heights(grid):
        heights = [0] * 5
        lines = grid.split("\n")
        if is_lock(grid):
            for line in lines[1:-1]:
                # i is row
                for c, char in enumerate(line):
                    if char == "#":
                        heights[c] += 1
        else:
            for line in reversed(lines[1:-1]):
                # i is row
                for c, char in enumerate(line):
                    if char == "#":
                        heights[c] += 1
        return heights

    locks, keys = [], []
    for grid in text.split("\n\n"):
        h = heights(grid)
        if is_lock(grid):
            locks.append(h)
        else:
            keys.append(h)

    def fit(lock, key):
        return all(a + b <= 5 for a, b in zip(lock, key))

    for l in locks:
        for k in keys:
            if fit(l, k):
                ans1 += 1

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
