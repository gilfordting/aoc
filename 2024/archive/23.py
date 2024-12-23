# Day       Time  Rank  Score       Time   Rank  Score
#  23   01:01:01  4390      0   01:14:03   3096      0

from collections import defaultdict
from functools import cache
from itertools import combinations

import networkx as nx
from tqdm import tqdm

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("23.txt", "r") as f:
        text = f.read()
    edges = defaultdict(set)
    vertices = set()
    for line in text.split("\n"):
        a, b = line.split("-")
        edges[a].add(b)
        edges[b].add(a)
        vertices.add(a)
        vertices.add(b)

    def is_triangle(a, b, c):
        return b in edges[a] and c in edges[a] and b in edges[c]

    def valid_name(s):
        return s[0] == "t"

    # part 1: get all triangles. Refactored later to use Part 2
    # for group in tqdm(combinations(vertices, 3), desc="Part 1"):
    #     a, b, c = group
    #     if is_triangle(a, b, c) and any(valid_name(s) for s in group):
    #         ans1 += 1

    all_dense_2 = set(frozenset([a, b]) for a, ls in edges.items() for b in ls)

    # part 2: largest dense graph
    @cache
    def get_dense_all(n):
        if n == 2:
            return all_dense_2
        all_graphs = set()
        for v in vertices:
            for dense_graph in get_dense_all(n - 1):
                if v in dense_graph:
                    continue
                # Check that v is connected to all nodes in this graph
                if set.intersection(edges[v], dense_graph) == dense_graph:
                    s = set.union(set(dense_graph), {v})
                    all_graphs.add(frozenset(s))
        return all_graphs

    # Refactored part 1
    for graph in get_dense_all(3):
        if any(valid_name(s) for s in graph):
            ans1 += 1

    last_graph = None
    for i in tqdm(range(2, len(vertices)), desc="Part 2"):
        all_dense = get_dense_all(i)
        if len(all_dense) == 0:
            break
        last_graph = all_dense

    ans2 = ",".join(sorted(last_graph.pop()))

    # Post-mortem: using networkx
    G = nx.Graph()
    for line in text.split("\n"):
        a, b = line.split("-")
        G.add_edge(a, b)
    all_cliques = list(nx.find_cliques(G))
    all_cliques.sort(key=len, reverse=True)
    biggest = all_cliques[0]
    ans2 = ",".join(sorted(biggest))

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
