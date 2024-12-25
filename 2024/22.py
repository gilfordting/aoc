# Day       Time  Rank  Score       Time   Rank  Score
#  22   03:54:38  8247      0   04:18:24   6038      0
import sys
from collections import defaultdict
from itertools import islice, pairwise

from tqdm import tqdm

sys.setrecursionlimit(10_000)


def groupwise(iterable, n=4):
    """
    Create an iterator of overlapping groups of size n from the input iterable.
    Similar to pairwise() but with configurable group size.

    Example:
        groupwise([1,2,3,4,5,6]) -> (1,2,3,4), (2,3,4,5), (3,4,5,6)
    """
    iterator = iter(iterable)
    window = tuple(islice(iterator, n))
    if len(window) == n:
        yield window
    for item in iterator:
        window = window[1:] + (item,)
        yield window


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("22.txt", "r") as f:
        text = f.read()

    def mix(a, b):
        return a ^ b

    def prune(a):
        return a % 16777216

    def next_random(x):
        x = prune(mix(x, x * 64))
        x = prune(mix(x, x // 32))
        x = prune(mix(x, x * 2048))
        return x

    def nth_secret(x, n=2000):
        if n == 0:
            return x
        return nth_secret(next_random(x), n - 1)

    def ones(x):
        return int(str(x)[-1])

    def get_prices(x):
        prices = []
        prices.append(ones(x))
        for _ in range(2000):
            x = next_random(x)
            prices.append(ones(x))
        return prices

    nums = []
    for num in text.split("\n"):
        num = int(num)
        ans1 += nth_secret(num)
        nums.append(num)

    all_pricelists = [get_prices(x) for x in nums]

    def get_deltas(prices):
        return [b - a for a, b in pairwise(prices)]

    all_deltas = [get_deltas(prices) for prices in all_pricelists]

    # scan and add to thing
    global_totals = defaultdict(int)
    for prices, deltas in tqdm(
        list(zip(all_pricelists, all_deltas)), desc="Part 2 computation"
    ):
        seen = set()
        for i, delta_group in enumerate(groupwise(deltas, n=4)):
            if delta_group in seen:
                continue
            seen.add(delta_group)
            global_totals[delta_group] += prices[i + 4]

    ans2 = max(global_totals.values())

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
