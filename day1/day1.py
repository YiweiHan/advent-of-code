from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

groups = [list(group) for k, group in groupby(lines, bool) if k]
sums_desc = sorted(map(lambda g: sum(map(lambda n: int(n), g)), groups), reverse=True)
print(sums_desc[0])
print(sum(sums_desc[0:3]))
