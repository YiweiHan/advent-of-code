import re
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

left = []
right = []

for line in lines:
    p = re.split("\\s+", line)
    l, r = int(p[0]), int(p[1])
    left.append(l)
    right.append(r)

left = sorted(left)
right = sorted(right)

sum = 0
for x, y in zip(left, right):
    sum = sum + abs(x - y)
print(sum)

right_occur = defaultdict(int)

for y in right:
    right_occur[y] = right_occur[y] + 1

sim = 0
for x in left:
    sim = sim + x * right_occur[x]

print(sim)
