from collections import Counter
from itertools import pairwise

if __name__ == "__main__":
    with open("02.txt", "r") as f:
        text = f.read()
    reports = []
    for line in text.split("\n"):
        levels = list(map(int, line.split(" ")))
        reports.append(levels)

    def is_safe(report):
        cond_1 = all(i < j for i, j in pairwise(report)) or all(
            i > j for i, j in pairwise(report)
        )
        cond_2 = all(1 <= abs(i - j) <= 3 for i, j in pairwise(report))
        return cond_1 and cond_2

    def is_safe_with_margin(report):
        return is_safe(report) or any(
            is_safe([report[j] for j in range(len(report)) if j != i])
            for i in range(len(report))
        )

    print(len([report for report in reports if is_safe(report)]))
    print(len([report for report in reports if is_safe_with_margin(report)]))
