from collections import defaultdict

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day07.txt") as f:
        data = f.read()
    data = [[c for c in line] for line in data.split('\n')]

    def part1():
        source = data[0].index('S') # S on line 1
        beams = set([source])
        splits = 0
        for line in data[1:]:
            # Line is the .'s and ^'s
            new_beams = set()
            removed_beams = set()
            for i, c in enumerate(line):
                if i in beams and c == '^':
                    # Split!
                    splits += 1
                    removed_beams.add(i)
                    if i-1 >= 0:
                        new_beams.add(i-1)
                    if i+1 < len(line):
                        new_beams.add(i+1)
            beams = (beams - removed_beams) | new_beams
        return splits
    
    def part2():
        source = data[0].index('S') # S on line 1
        positions = {} # map particle position: # of originating timelines
        positions[source] = 1
        for line in data[1:]:
            next_positions = defaultdict(int)
            for i, c in enumerate(line):
                if i not in positions:
                    continue
                if c == '.': # continue on
                    next_positions[i] += positions[i]
                    continue
                # '^', timeline split
                if i-1 >= 0:
                    next_positions[i-1] += positions[i]
                if i+1 < len(line):
                    next_positions[i+1] += positions[i]
            positions = next_positions
        return sum(positions.values())

    
    ans1 = part1()
    ans2 = part2()
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
