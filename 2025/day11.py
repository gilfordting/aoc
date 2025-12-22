import itertools
from collections import defaultdict

import networkx as nx

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day11.txt") as f:
        data = f.read()
    
    devices = []
    for line in data.split('\n'):
        src, dests = line.split(': ')
        dests = dests.split(' ')
        devices.append((src, dests))
    
    def part1():
        G = nx.DiGraph()
        for s in ['you', 'out']:
            G.add_node(s)
        for src, _ in devices:
            G.add_node(src)
        for src, dests in devices:
            for dest in dests:
                G.add_edge(src, dest)
        return len(list(nx.all_simple_paths(G, 'you', 'out')))
    
    def part2():
        G = nx.DiGraph()
        G.add_node('out')
        for src, _ in devices:
            G.add_node(src)
        for src, dests in devices:
            for dest in dests:
                G.add_edge(src, dest)
        
        # Use topological order
        # For each node we process, total number of ways to get to an associated state is sum of ways to get to nodes from incoming edges
        n_paths = defaultdict(int)
        # State is node name, whether 'dac' visited, whether 'fft' visited
        n_paths[('svr', False, False)] = 1
        for node in nx.topological_sort(G):
            # If we're at 'dac' or 'fft', corresponding state must flip to True
            if node == 'dac':
                for source, _ in G.in_edges(nbunch=node):
                    for fft_visited in [True, False]:
                        n_paths[(node, True, fft_visited)] += sum(
                            n_paths[(source, dac_visited, fft_visited)] for dac_visited in [True, False]
                        )
                continue
            
            if node == 'fft':
                for source, _ in G.in_edges(nbunch=node):
                    for dac_visited in [True, False]:
                        n_paths[(node, dac_visited, True)] += sum(
                            n_paths[(source, dac_visited, fft_visited)] for fft_visited in [True, False]
                        )
                continue


            # Look at all the incoming edges. Source nodes must already have been processed; aggregate over them
            for source, _ in G.in_edges(nbunch=node):
                for dac_visited, fft_visited in itertools.product([True, False], [True, False]):
                    n_paths[(node, dac_visited, fft_visited)] += n_paths[(source, dac_visited, fft_visited)]
        
        return n_paths[('out', True, True)]


    ans1 = part1()
    ans2 = part2()
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
