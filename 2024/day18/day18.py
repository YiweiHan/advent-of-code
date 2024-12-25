from collections import deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

b = []
for l in lines:
    b.append(tuple(map(int, l.split(","))))

start = (0, 0)
dim = 71
n_fell = 1024
end = (dim - 1, dim - 1)


def nexts(cur):
    r, c = cur
    next_pos = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
    return list(filter(lambda p: 0 <= p[0] < dim and 0 <= p[1] < dim, next_pos))


def sim(n_fell):
    fell = set(b[:n_fell])

    visited = set()

    q = deque([(start, 0)])
    min_steps = None
    while q:
        cur, steps = q.popleft()
        if cur == end:
            if min_steps is None or steps < min_steps:
                min_steps = steps
            continue
        if cur in visited:
            continue
        visited.add(cur)

        ns = nexts(cur)
        ns = list(filter(lambda p: p not in fell, ns))
        for n in ns:
            q.append((n, steps + 1))
    return min_steps


print(sim(n_fell))

for n_fell in range(len(b)):
    res = sim(n_fell)
    if res is None:
        bb = b[n_fell - 1]
        print(f"{bb[0]},{bb[1]}")
        break
