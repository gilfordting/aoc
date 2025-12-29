# process smth like:
# 5:
# ###
# .#.
# ###
from pprint import pprint


def process_shape(i, s):
    label, shape = s.split(":\n")
    assert int(label) == i
    # turn string into bool matrix
    return [[c == "#" for c in line] for line in shape.splitlines()]


# process smth like:
# 4x4: 0 0 0 0 2 0
# returns n_rows, n_cols, quantities of each shape (list)
def process_region(s):
    dims, qtys = s.split(": ")
    width, height = dims.split("x")
    n_cols, n_rows = int(width), int(height)
    qtys = tuple(int(s) for s in qtys.split(" "))
    return n_rows, n_cols, qtys


# shapes are all bool matrices
# regions are size dims and then quantities
def process(data):
    data = data.split("\n\n")
    shapes, regions = data[:-1], data[-1]
    shapes = [process_shape(i, s) for i, s in enumerate(shapes)]
    regions = [process_region(line) for line in regions.splitlines()]
    return shapes, regions


def shape_area(shape):
    area = sum(1 for row in shape for v in row if v)
    return area


# naive possible: everything goes in its own 3x3 grid
def possible(shapes, region):
    n_row, n_col, qtys = region
    return n_row // 3 * n_col // 3 > sum(qtys)


def impossible(shapes, region):
    # Look at sum of all
    n_row, n_col, qtys = region

    total_req = sum(count * shape_area(shapes[i]) for i, count in enumerate(qtys))
    return n_row * n_col < total_req


def part1(shapes, regions):
    ans = 0
    for region in regions:
        if not impossible(shapes, region) or possible(shapes, region):
            print(region)
            ans += 1
    return ans


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day12.txt") as f:
        data = f.read()
    shapes, regions = process(data)

    ans1 = part1(shapes, regions)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
