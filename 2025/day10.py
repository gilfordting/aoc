import numpy as np
import scipy.optimize

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day10.txt") as f:
        data = f.read()
    machines = []
    for line in data.split('\n'):
        paren_i = line.index('(')
        square_l, square_r = 0, line.index(']')
        lights = tuple(c == '#' for c in line[square_l+1:square_r])
        cbrace_i = line.index('{')
        wiring = [
            set(int(i) for i in token[1:-1].split(','))
            for token in line[paren_i:cbrace_i-1].split(' ')
        ]
        joltages = tuple(int(i) for i in line[cbrace_i+1:-1].split(','))
        machines.append((lights, wiring, joltages))
    
    def toggle_lights(state, button):
        return tuple(
            not s if i in button else s
            for i, s in enumerate(state)
        )
    
    def min_presses_lights(lights, wiring):
        init = (False,) * len(lights)
        # Anything in `q` must also be in `visited`
        q = [(init, 0)]
        visited = set([init])
        while q:
            state, dist = q.pop(0)
            if state == lights:
                return dist
            # Visit neighbors
            for button in wiring:
                next_state = toggle_lights(state, button)
                if next_state in visited:
                    continue
                visited.add(next_state)
                q.append((next_state, dist+1))

    
    def part1():
        return sum(
            min_presses_lights(lights, wiring) for lights, wiring, _ in machines
        )
    
    
    def incr_joltages(joltages, button):
        return tuple(
            v+1 if i in button else v
            for i, v in enumerate(joltages)
        )


    def min_presses_joltage(joltages, wiring):
        # A encodes button layouts
        # B is desired states
        # Solve Ax = B, subject to x as nonnegative integers (ILP).
        cols = []
        for button in wiring:
            a = np.zeros(len(joltages), dtype=int)
            for idx in button:
                a[idx] = 1
            cols.append(a)
        A = np.array(cols).T  # shape: (n_lights, n_buttons)
        B = np.array(joltages)

        n_buttons = A.shape[1]
        c = np.ones(n_buttons, dtype=int)  # weighting function; minimize sum of vector
        bounds = [(0, None) for _ in range(n_buttons)] # allowed range is >= 0
        res = scipy.optimize.linprog(
            c,
            A_eq=A,
            b_eq=B,
            bounds=bounds,
            method="highs",
            integrality=np.ones(n_buttons, dtype=bool)  # all integers
        )
        presses = np.rint(res.x).astype(int)
        return presses.sum()


    def part2():
        return sum(min_presses_joltage(joltages, wiring) for _, wiring, joltages in machines)

    ans1 = part1()
    ans2 = part2()
                
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
