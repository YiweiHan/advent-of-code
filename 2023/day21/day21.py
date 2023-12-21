from itertools import pairwise
from collections import deque

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

rows, cols = len(grid), len(grid[0])

start = None
plots = set()
for r in range(rows):
    for c in range(cols):
        v = grid[r][c]
        if v == "S":
            start = (r, c)
        if v == "." or v == "S":
            plots.add((r, c))


def explore(max_steps):
    def is_plot(p):
        return (p[0] % rows, p[1] % cols) in plots

    min_steps_away = {}
    q = deque()
    q.append((start, 0))
    while len(q):
        cur, steps_taken = q.popleft()
        if cur in min_steps_away:
            continue
        min_steps_away[cur] = steps_taken

        if steps_taken == max_steps:
            continue

        nexts = [(cur[0] + d[0], cur[1] + d[1]) for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        nexts = list(filter(lambda p: is_plot(p), nexts))
        q.extend([(pos, steps_taken + 1) for pos in nexts])
    return sum(min_steps <= max_steps and (max_steps - min_steps) % 2 == 0 for _, min_steps in min_steps_away.items())

# part 1
print(explore(64))

# part 2
max_steps = 26501365
cycles = max_steps // rows
cycle_steps = [explore(steps) for steps in range(rows // 2, 3 * rows, rows)]
sequences = [cycle_steps[0]]
diffs = cycle_steps
for _ in range(2):
    diffs = [y - x for x, y in pairwise(diffs)]
    sequences.append(diffs[0])
for _ in range(1, cycles + 1):
    sequences[0] = sequences[0] + sequences[1]
    sequences[1] = sequences[1] + sequences[2]
print(sequences[0])
