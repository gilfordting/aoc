# Day       Time  Rank  Score       Time   Rank  Score
#   5   00:07:02   666      0   00:23:11   2017      0

import re
from collections import Counter
from graphlib import TopologicalSorter
from itertools import pairwise, permutations

if __name__ == "__main__":
    with open("05.txt", "r") as f:
        text = f.read()
    rules, updates = text.split("\n\n")
    rules = rules.split("\n")
    updates = updates.split("\n")

    updates = [list(map(int, line.split(","))) for line in updates]
    orderings = []
    edges = {}
    for rule in rules:
        a, b = rule.split("|")
        a, b = int(a), int(b)
        # a comes before b
        orderings.append((a, b))
        edges.setdefault(a, []).append(b)

    def is_valid(update):
        for a, b in orderings:
            if a in update and b in update and update.index(a) > update.index(b):
                return False
        return True

    def middle_val(l):
        i = (len(l) - 1) // 2
        return l[i]

    # def reordered(update):
    #     # Assume no cycles.
    #     nodes = set(update)
    #     visited = set()
    #     order = []

    #     def dfs(node):
    #         if node in visited:
    #             return

    #         if node in edges:
    #             neighbors = edges[node]
    #             for neighbor in neighbors:
    #                 if neighbor in nodes:
    #                     dfs(neighbor)

    #         visited.add(node)
    #         order.append(node)

    #     for node in nodes:
    #         if node not in visited:
    #             dfs(node)

    #     assert set(order) == nodes
    #     return order

    # More intelligent solution
    # def reordered(update):
    #     update = update[:]
    #     while not is_valid(update):
    #         for i in range(len(update)):
    #             for j in range(i + 1, len(update)):
    #                 if update[j] in edges and update[i] in edges[update[j]]:
    #                     update[i], update[j] = update[j], update[i]
    #     return update

    #  Or:
    def reordered(update):
        nodes = set(update)
        edges_i = {
            a: [i for i in l if i in nodes] for a, l in edges.items() if a in nodes
        }
        ts = TopologicalSorter(edges_i)
        return list(ts.static_order())[::-1]

    total = 0
    total_2 = 0
    for update in updates:
        if is_valid(update):
            total += middle_val(update)
        else:
            total_2 += middle_val(reordered(update))
    print(total)
    print(total_2)
