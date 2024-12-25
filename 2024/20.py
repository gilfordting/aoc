# Day       Time  Rank  Score       Time   Rank  Score
#  20   00:46:46  2479      0   01:10:01   1682      0


import networkx as nx
from tqdm import tqdm

deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}


def process_grid_input(text):
    lines = text.split("\n")
    n_rows, n_cols = len(lines), len(lines[0])
    grid = [[c for c in line] for line in lines]

    def in_bounds(r, c):
        return 0 <= r < n_rows and 0 <= c < n_cols

    def get_neighbors(r, c):
        for dr, dc in deltas:
            next_r, next_c = r + dr, c + dc
            if in_bounds(next_r, next_c):
                yield next_r, next_c

    def grid_iter():
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                yield r, c, val

    return grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("20.txt", "r") as f:
        text = f.read()

    # Grid input
    grid, n_rows, n_cols, in_bounds, get_neighbors, grid_iter = process_grid_input(text)

    # Processing the input
    G = nx.grid_graph((n_rows, n_cols))
    start, end = None, None
    for r, c, val in grid_iter():
        if val == "S":
            start = (r, c)
        elif val == "E":
            end = (r, c)
        elif val == "#":
            G.remove_node((r, c))

    dist = nx.shortest_path_length(G, start)
    fastest_time = dist[end]
    print(fastest_time)

    # Part 1. Did not realize that you did not have to verify a cheat's savings by re-running Dijkstra's -- you can just use the distances computed by nx.shortest_path_length.

    # generate all possible cheats
    def get_all_cheats():
        for r in range(n_rows):
            for c in range(n_cols):
                if grid[r][c] == "#":
                    continue
                # Valid starting position
                for dr1, dc1 in deltas:
                    int_r, int_c = r + dr1, c + dc1
                    if not in_bounds(int_r, int_c) or grid[int_r][int_c] != "#":
                        continue
                    for dr2, dc2 in deltas:
                        next_r, next_c = int_r + dr2, int_c + dc2
                        if not in_bounds(next_r, next_c) or grid[next_r][next_c] == "#":
                            continue
                        yield (r, c), (int_r, int_c), (next_r, next_c)

    cheats = list(get_all_cheats())
    for start_pos, int_pos, end_pos in tqdm(cheats):
        if start_pos == end_pos:
            continue
        G.add_node(int_pos)
        G.add_edge(start_pos, int_pos)
        G.add_edge(int_pos, end_pos)
        t = nx.shortest_path_length(G, start, end)
        if fastest_time - t >= 100:
            ans1 += 1
        G.remove_edge(start_pos, int_pos)
        G.remove_edge(int_pos, end_pos)
        G.remove_node(int_pos)
    ans1 //= 2

    # Part 2: generate all possible cheats
    # go from an earlier non-wall square to a later non-wall square, must use <= 20 seconds.
    # then calculate the amount of time you save

    def cheat_length(start, end):
        s_r, s_c = start
        e_r, e_c = end
        return abs(s_r - e_r) + abs(s_c - e_c)

    for start_r, start_c, start_val in tqdm(grid_iter()):
        if start_val == "#":
            continue
        for end_r, end_c, end_val in grid_iter():
            if end_val == "#":
                continue
            start_pos = (start_r, start_c)
            end_pos = (end_r, end_c)
            if dist[end_pos] < dist[start_pos]:
                continue
            l = cheat_length(start_pos, end_pos)
            if l > 20:
                continue
            usual_time = dist[end_pos] - dist[start_pos]
            savings = usual_time - l
            if savings >= 100:
                ans2 += 1

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
