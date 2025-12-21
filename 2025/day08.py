import math

import networkx as nx

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day08.txt") as f:
        data = f.read()
    coords = []
    for line in data.split('\n'):
        l = list(map(int, line.split(',')))
        x, y, z = l
        coords.append((x, y, z))
    coords.sort(key=lambda x: x[0]**2 + x[1]**2 + x[2]**2)

    def dist(coord1, coord2):
        return sum((i-j)**2 for i, j in zip(coord1, coord2))
    
    def part1():
        N_JOINS = 1000
        G = nx.Graph()
        for i in range(len(coords)):
            G.add_node(i)
        # Get all pairs
        edges = []
        for i, c_i in enumerate(coords):
            for j, c_j in enumerate(coords):
                if j <= i:
                    continue
                cdist = dist(c_i, c_j)
                edges.append((i, j, cdist))
        edges.sort(key=lambda x: x[2])
        # add edges that correspond
        for i, j, cdist in edges[:N_JOINS]:
            G.add_edge(i, j)
        # Return a list of the sizes of the connected components
        sizes = [len(c) for c in nx.connected_components(G)]
        sizes.sort()
        return math.prod(sizes[-3:])
    
    def part2():
        G = nx.Graph()
        for i in range(len(coords)):
            G.add_node(i)
        # Get all pairs
        edges = []
        for i, c_i in enumerate(coords):
            for j, c_j in enumerate(coords):
                if j <= i:
                    continue
                cdist = dist(c_i, c_j)
                edges.append((i, j, cdist))
        edges.sort(key=lambda x: x[2])
        last_edge = None
        while nx.number_connected_components(G) != 1:
            i, j, _ = edges.pop(0)
            G.add_edge(i, j)
            last_edge = (i, j)
        i, j = last_edge
        return coords[i][0] * coords[j][0]
        
    
    ans1 = part1()
    ans2 = part2()
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
