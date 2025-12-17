

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day05.txt") as f:
        data = f.read()
    
    _ranges, ingrs = data.split('\n\n')
    ranges = [] 
    for line in _ranges.split('\n'):
        left, right = line.split('-')
        ranges.append((int(left), int(right)))
    ingrs = [int(i) for i in ingrs.split('\n')]

    def fresh(i):
        return any(left <= i <= right for left, right in ranges)
    
    ans1 = sum(1 for i in ingrs if fresh(i))

    # Merge ranges
    ranges.sort()
    ans2 = 0
    curr_range = None
    for left, right in ranges:
        if curr_range is None:
            curr_range = (left, right)
        curr_left, curr_right = curr_range
        # In range of current one
        if curr_left <= left <= curr_right:
            curr_right = max(curr_right, right)
            curr_range = (curr_left, curr_right)
            continue
        # Otherwise, disjoint
        ans2 += curr_right - curr_left + 1
        curr_range = (left, right)
    
    ans2 += (curr_range[1] - curr_range[0] + 1)


    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
