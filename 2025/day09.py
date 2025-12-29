from itertools import combinations, pairwise


# Opposite corners; should be sorted
def area(x1, y1, x2, y2):
    assert x1 <= x2 and y1 <= y2
    return (x2 - x1 + 1) * (y2 - y1 + 1)


# Works for both rectangles and segments; for segments we have the property that one coordinate stays the same
def canonize(x1, y1, x2, y2):
    return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


# Takes pairs of coordinates as inputs, canonizes and sorts by:
# - area, for rectangles
# - length, for edges
def process_pairs(pairs):
    return sorted(
        (canonize(x1, y1, x2, y2) for (x1, y1), (x2, y2) in pairs),
        key=lambda x: area(*x),
        reverse=True,
    )


# Turns `tiles` into two canonized lists:
# - rectangles, defined by red corners
# - edges, defined by endpoints (red)
def process(red_tiles):
    rects = process_pairs(combinations(red_tiles, 2))
    edges = process_pairs(pairwise(red_tiles + [red_tiles[0]]))
    return rects, edges


def part1(rects, edges):
    return area(*rects[0])


def intersects(rect, edge):
    r_x1, r_y1, r_x2, r_y2 = rect
    e_x1, e_y1, e_x2, e_y2 = edge
    return e_x1 < r_x2 and e_y1 < r_y2 and e_x2 > r_x1 and e_y2 > r_y1


def part2(rects, edges):
    for rect in rects:
        if any(intersects(rect, edge) for edge in edges):
            continue
        return area(*rect)


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day09.txt") as f:
        data = f.read()
    red_tiles = []
    for line in data.split("\n"):
        r, c = line.split(",")
        red_tiles.append((int(r), int(c)))
    rects, edges = process(red_tiles)

    ans1 = part1(rects, edges)
    ans2 = part2(rects, edges)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
