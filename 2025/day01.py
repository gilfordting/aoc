def rotate(num, direction, count):
    num_zeros = 0
    if direction == "L":
        # subtract -- what's the distance from 0?
        if num > count:
            return num - count, num_zeros
        else:
            # get to 0
            if num != 0:
                count -= num
                num = 0
                num_zeros += 1
            num_zeros += count // 100
            num -= count
            num %= 100
            return num, num_zeros
    # addition
    # will it even get to 0?
    rem = 100 - num
    if rem > count:
        return num + count, num_zeros
    if num != 0:
        num = 0
        count -= rem
        num_zeros += 1
    num_zeros += count // 100
    num += count
    num %= 100
    return num, num_zeros


if __name__ == "__main__":
    ans1, ans2 = 0, 0
    num = 50

    with open("data/day01.txt") as f:
        for line in f:
            direction = line[0]
            count = int(line[1:])
            num, num_zeros = rotate(num, direction, count)
            if num == 0:
                ans1 += 1
            ans2 += num_zeros

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
