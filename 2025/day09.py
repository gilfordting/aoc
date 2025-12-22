from itertools import combinations

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day09.txt") as f:
        data = f.read()
    tiles = []
    for line in data.split('\n'):
        r, c = line.split(',')
        tiles.append((int(r), int(c)))
    
    def area(tile1, tile2):
        return (abs(tile1[0] - tile2[0])+1) * (abs(tile1[1] - tile2[1])+1)
    
    def part1():
        # Naive pairwise
        best_area = -float('inf')
        for t_i, t_j in combinations(tiles, 2):
            best_area = max(best_area, area(t_i, t_j))
        return best_area
    
    # Whether a tile pair (indices) falls within the region
    def valid(i, j):
        assert i < j
        tile1 = tiles[i]
        tile2 = tiles[j]
        # bounding box
        low_r, high_r = (tile1[0], tile2[0]).sort()
        low_c, high_c = (tile1[1], tile2[1]).sort()
        


        def in_bb(r, c):
            return low_r <= r <= high_r and low_c <= c <= high_c
        # check that everything on the path stays OUTSIDE the bb, i.e. bb is subset of traced path

        # Traced path needs to stay outside bb, or be on the edge

        

    
    def part2():
        return 0

    ans1 = part1()
    ans2 = part2()
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
