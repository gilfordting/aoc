def good_rolls(grid):
    n_rows, n_cols = len(grid), len(grid[0])

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols
    
    def neighbors(r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                if not in_bounds(r+dr, c+dc):
                    continue
                yield (r+dr, c+dc)

    def is_good(r, c):
        return sum(1 for neighbor_r, neighbor_c in neighbors(r, c) if grid[neighbor_r][neighbor_c] == '@') < 4
    
    ans = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == '@' and is_good(r, c):
                ans += 1
    return ans

def num_removable(grid):
    n_rows, n_cols = len(grid), len(grid[0])

    def is_roll(r, c):
        return grid[r][c] == "@"

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols
    
    def neighbors(r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                if not in_bounds(r+dr, c+dc):
                    continue
                yield (r+dr, c+dc)

    def is_good(r, c):
        assert is_roll(r, c)
        return sum(1 for neighbor_r, neighbor_c in neighbors(r, c) if is_roll(neighbor_r, neighbor_c)) < 4
    
    def done():
        for r in range(n_rows):
            for c in range(n_cols):
                if is_roll(r, c) and is_good(r, c):
                    return False
        return True
    
    ans = 0

    while not done():
        found = []
        # iteratively remove
        for r in range(n_rows):
            for c in range(n_cols):
                if is_roll(r, c) and is_good(r, c):
                    found.append((r, c))
        for r, c in found:
            grid[r][c] = '.'
            ans += 1
    
    return ans
    


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day04.txt") as f:
        data = f.read()
        grid = [list(line) for line in data.split('\n')]
        ans1 += good_rolls(grid)
        ans2 += num_removable(grid)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
