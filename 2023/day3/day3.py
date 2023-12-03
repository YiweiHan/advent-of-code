import re
from itertools import product, accumulate
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


nums = []
symbols = []

for r, line in enumerate(lines):
    for m in re.finditer(r"[0-9]+", line):
        nums.append((r, (m.span()[0], m.span()[1] - 1), int(m.group())))
    for s in re.finditer(r"[^0-9.]", line):
        symbols.append((r, s.span()[0], s.group()))

total = 0
seen_nums = set()

maybe_gears = defaultdict(list)

for s in symbols:
    row_start, row_end = s[0] - 1, s[0] + 1
    col_start, col_end = s[1] - 1, s[1] + 1
    for coord in product(range(row_start, row_end + 1), range(col_start, col_end + 1)):
        for n in nums:
            if n in seen_nums:
                continue
            if coord[0] == n[0] and coord[1] in set(range(n[1][0], n[1][1] + 1)):
                total = total + n[2]
                seen_nums.add(n)
                if s[2] == "*":
                    maybe_gears[s].append(n[2])

# part 1
print(total)

# part 2
total_gear_ratio = 0
for _, nums in maybe_gears.items():
    if len(nums) > 1:
        total_gear_ratio = total_gear_ratio + list(accumulate(nums, lambda x, y: x * y))[-1]

print(total_gear_ratio)
