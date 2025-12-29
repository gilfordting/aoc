import itertools
from pprint import pprint

import numpy as np
from tqdm import tqdm


# process smth like:
# 5:
# ###
# .#.
# ###
def process_shape(i, s):
    label, shape = s.split(':\n')
    assert int(label) == i
    # turn string into bitmatrix
    return [
        [c == '#' for c in l] for l in shape.splitlines()
    ]

# process smth like:
# 4x4: 0 0 0 0 2 0
# returns n_rows, n_cols, quantities of each shape (list)
def process_region(s):
    dims, qtys = s.split(': ')
    width, height = dims.split('x')
    n_cols, n_rows = int(width), int(height)
    qtys = tuple(int(s) for s in qtys.split(' '))
    return n_rows, n_cols, qtys

def process(data):
    data = data.split('\n\n')
    shapes, regions = data[:-1], data[-1]
    shapes = [process_shape(i, s) for i, s in enumerate(shapes)]
    regions = [process_region(line) for line in regions.splitlines()]
    return shapes, regions

def transform(arr, vflip, hflip, n_rotate):
    if vflip:
        arr = np.flipud(arr)
    if hflip:
        arr = np.fliplr(arr)
    arr = np.rot90(arr, k=n_rotate)
    # lastly, turn into tuple version
    return tuple(tuple(bool(x) for x in row) for row in arr)

# takes shape as bitmatrix, return set of tuples of tuples of bools
def permute(shape):
    arr = np.array(shape)
    return set(
        transform(arr, vflip, hflip, n_rotate)
        for vflip in [True, False]
        for hflip in [True, False]
        for n_rotate in range(4)
    )

# See if we can place this shape at (r, c) on the grid
def place(grid, shape, r, c):
    new_grid = [
        [v for v in row]
        for row in grid
    ]
    for dr, row in enumerate(shape):
        for dc, shape_tile in enumerate(row):
            if shape_tile:
                if grid[r+dr][c+dc]:
                    # conflict
                    return None, False
                new_grid[r+dr][c+dc] = True

    return new_grid, True

def fits_all(region, shapes):
    n_rows, n_cols, qtys = region
    shapes = [permute(shape) for shape in shapes]
    def works(grid, remaining):
        shape_i = None
        # Pick a shape to place
        for i, count in enumerate(remaining):
            if count != 0:
                shape_i = i
                break
        # No more shapes need to be placed
        if shape_i is None:
            return True
        
        new_rem = tuple(v-1 if i == shape_i else v for i, v in enumerate(remaining))
        # Consider all possible permutations of that shape
        for shape in shapes[shape_i]:
            # And all the places we can put it
            for r, c in itertools.product(range(n_rows-2), range(n_cols-2)):
                new_grid, ok = place(grid, shape, r, c)
                if not ok:
                    continue
                if works(new_grid, new_rem):
                    return True
        return False
                

    return works([[False] * n_cols for _ in range(n_rows)], qtys)

def part1(shapes, regions):
    return sum(
        1 for region in tqdm(regions)
        if fits_all(region, shapes)
    )

def part2(shapes, regions):
    pass

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day12.txt") as f:
        data = f.read()
    shapes, regions = process(data)

    ans1 = part1(shapes, regions)
    ans2 = part2(shapes, regions)
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
