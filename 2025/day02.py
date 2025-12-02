import math


def range_sum(a, b):
    return (b - a + 1) * (a-1) + (b-a+1)*(b-a+2) // 2

if __name__ == "__main__":
    ans1, ans2 = 0, 0
    num = 50

    def invalid_id_sum_in(lo, hi, part2=False):
        lo_len, hi_len = len(str(lo)), len(str(hi))
        assert lo_len == hi_len
        if not part2:
            if lo_len % 2 == 1:
                return 0
            # 2-digit: 11
            # 4-digit: 101
            # 6-digit: 1001
            factor = 10 ** (lo_len // 2) + 1
            lo_multiple = math.ceil(lo / factor)
            hi_multiple = math.floor(hi / factor)
            if lo_multiple > hi_multiple:
                return 0

            # what is sum of a to b, increasing?
            # this is (b - a + 1) * (a-1) + (b-a+1)(b-a+2)/2
            
            # sum factor * range sum
            return factor * range_sum(lo_multiple, hi_multiple)
            # return hi_multiple - lo_multiple + 1
        # repetition factor can be any multiple of the length
        # (how many times it repeats)
        counted = set()
        ans = 0
        for repeat_factor in range(2, lo_len + 1):
            if lo_len % repeat_factor != 0:
                continue
            group_size = lo_len // repeat_factor
            factor = 1
            for _ in range(repeat_factor-1):
                factor *= 10**group_size
                factor += 1
            lo_multiple = math.ceil(lo / factor)
            hi_multiple = math.floor(hi / factor)
            if lo_multiple > hi_multiple:
                continue
            for i in range(lo_multiple, hi_multiple+1):
                n = i * factor
                if n in counted:
                    continue
                counted.add(n)
                print(n)
                ans += n
        return ans

    def all_id_sums(lo, hi, part2=False):
        # print(lo, hi)
        lo_len, hi_len = len(str(lo)), len(str(hi))
        # Bucket into proper ranges
        ranges = []
        if lo_len == hi_len:
            ranges.append((lo, hi))
        else:
            ranges.append((lo, 10 ** lo_len - 1))
            ranges.append((10 ** (hi_len-1), hi))
            for l in range(lo_len + 1, hi_len):
                ranges.append(10**(l-1), 10**l - 1)
        # print(ranges)
        # Process each range individually
        ans = sum(invalid_id_sum_in(lo, hi, part2=part2) for lo, hi in ranges)
        # print(ans)
        return ans

    with open("data/day02.txt") as f:
        data = f.read()
        for token in data.split(","):
            first, last = token.split("-")
            ans1 += all_id_sums(int(first), int(last))
            ans2 += all_id_sums(int(first), int(last), part2=True)

    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
