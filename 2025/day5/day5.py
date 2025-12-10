from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

ranges, ids = [list(g) for k, g in groupby(lines, key=bool) if k]
ranges = [list(map(lambda x: int(x), r.split("-"))) for r in ranges]
ids = [int(x) for x in ids]

c = 0
for i in ids:
    for start, end in ranges:
        if start <= i <= end:
            c += 1
            break
print(c)

ranges = sorted(ranges, key=lambda x: x[0])

merged = []
for a, b in ranges:
    if not merged or a > merged[-1][1]:
        merged.append([a, b])
    else:
        merged[-1][1] = max(merged[-1][1], b)

c2 = 0
for a, b in merged:
    c2 += len(range(a, b)) + 1
print(c2)
