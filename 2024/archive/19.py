# Day       Time  Rank  Score       Time   Rank  Score
#  19   00:03:20   223      0   00:05:51    266      0

from functools import cache

from tqdm import tqdm

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("19.txt", "r") as f:
        text = f.read()

    patterns, designs = text.split("\n\n")
    patterns = patterns.split(", ")
    designs = designs.split("\n")

    @cache
    def is_possible(design):
        if design == "":
            return True
        return any(
            design.startswith(p) and is_possible(design[len(p) :]) for p in patterns
        )

    @cache
    def num_ways(design):
        if design == "":
            return 1

        ways = 0
        for p in patterns:
            if design.startswith(p):
                ways += num_ways(design[len(p) :])
        return ways

    for design in tqdm(designs):
        if is_possible(design):
            ans1 += 1
            ans2 += num_ways(design)

    print(ans1)
    print(ans2)
