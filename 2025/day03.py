def max_joltage_1(s):
    ans = 0
    for i, c_i in enumerate(s):
        for c_j in s[i+1:]:
            ans = max(ans, 10 * int(c_i) + int(c_j))
    return ans

def max_joltage_2(s):
    # dp[i][j]: max joltage considering everything up to i, of length j
    # dp[i][j]: max(
    #  dp[i-1][j],
    #  dp[i-1][j-1] * 10 + current
    # )
    # just have running max for each possible length
    maxes = [0] * 13
    for c in s:
        next_maxes = [0] * 13
        for l in range(1, 13):
            next_maxes[l] = max(maxes[l], maxes[l-1] * 10 + int(c))
        maxes = next_maxes
    return maxes[-1]


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    with open("data/day03.txt") as f:
        data = f.read()
        for s in data.split('\n'):
            ans1 += max_joltage_1(s)
            ans2 += max_joltage_2(s)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
