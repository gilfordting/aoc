from collections import Counter

if __name__ == "__main__":
    with open("01.txt", "r") as f:
        text = f.read()
    ls_a, ls_b = [], []
    for line in text.split("\n"):
        a, b = line.split("   ")
        a, b = int(a), int(b)
        ls_a.append(a)
        ls_b.append(b)
    # Part 1
    # ls_a.sort()
    # ls_b.sort()
    # print(sum(abs(a - b) for a, b in zip(ls_a, ls_b)))
    # Part 2
    vals = Counter(ls_b)
    print(sum(v * vals.get(v, 0) for v in ls_a))
