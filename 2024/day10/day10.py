from collections import defaultdict, deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)

grid = []
for l in lines:
    grid.append([int(x) for x in l])


heads = []
for r in range(dim):
    for c in range(dim):
        if grid[r][c] == 0:
            heads.append((r, c))


def nexts(cur):
    r, c = cur
    next_pos = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
    return list(filter(lambda p: 0 <= p[0] < dim and 0 <= p[1] < dim, next_pos))


def get_score(use_visisted):
    scores = defaultdict(int)
    visited = set()
    q = deque()
    for h in heads:
        q.append((h, h))

    while len(q):
        cur, head = q.pop()
        if use_visisted and (cur, head) in visited:
            continue
        visited.add((cur, head))
        cur_elev = grid[cur[0]][cur[1]]
        if cur_elev == 9:
            scores[head] = scores[head] + 1
            continue
        next_coords = nexts(cur)
        next_coords = list(filter(lambda p: grid[p[0]][p[1]] - cur_elev == 1, next_coords))
        for n in next_coords:
            q.append((n, head))
    s = 0
    for head, score in scores.items():
        s = s + score
    return s


print(get_score(True))
print(get_score(False))
