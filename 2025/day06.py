import math

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day06.txt") as f:
        data = f.read()
    
    nums = []
    ops = None
    for line in data.split('\n'):
        line = [token for token in line.split(' ') if token != ""]
        if line[0] == "*":
            ops = line
        else:
            nums.append([int(i) for i in line])

    
    def problem1(i):
        if ops[i] == "*":
            return math.prod(arr[i] for arr in nums)
        return sum(arr[i] for arr in nums)
    
    for i in range(len(ops)):
        ans1 += problem1(i)
    
    data = data.split('\n')
    nums = [[] for _ in range(len(data)-1)]
    # Look at last line
    last_i = None
    for i, c in enumerate(data[-1]):
        if c == " ":
            continue
        if last_i is None:
            last_i = i
            continue
        for j, ls in enumerate(nums):
            ls.append(data[j][last_i:i-1])
        last_i = i
    for i, ls in enumerate(nums):
        ls.append(data[i][last_i:])

    def problem2(i):
        # "transpose" the numbers
        width = len(nums[0][i])
        operands = []
        for j in range(width):
            # assemble the number
            num_s = ""
            for arr in nums:
                s = str(arr[i])
                # Get the one at width - 1 - j
                if width - 1 - j < len(s):
                    num_s += s[width-1-j]
                else:
                    num_s += "0"
            operands.append(int(num_s))

        if ops[i] == "*":
            return math.prod(operands)
        return sum(operands)
    
    for i in range(len(ops)):
        ans2 += problem2(i)
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
