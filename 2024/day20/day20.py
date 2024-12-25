from itertools import combinations

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)


def value(p):
    return lines[p[0]][p[1]]


track = set()
start = end = None
for r in range(dim):
    for c in range(dim):
        v = value((r, c))
        if v != '#':
            track.add((r, c))
        if v == 'S':
            start = (r, c)
        if v == 'E':
            end = (r, c)


def nexts(cur):
    r, c = cur
    return [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]


steps = {start: 0}
fullpath = [start]

q = [start]
while q:
    cur = q.pop()
    ns = nexts(cur)
    for n in ns:
        if n in track and n not in steps:
            steps[n] = steps[cur] + 1
            fullpath.append(n)
            q.append(n)

s = s2 = 0
for (p1, step1), (p2, steps2) in combinations(steps.items(), 2):
    dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    saved = steps2 - step1 - dist
    if saved >= 100:
        if dist == 2:
            s += 1
        if dist <= 20:
            s2 += 1

print(s)
print(s2)
