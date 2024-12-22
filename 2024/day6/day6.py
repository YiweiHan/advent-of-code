with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)

start = None
obs = set()
for r in range(dim):
    for c in range(dim):
        v = lines[r][c]
        if v == '^':
            start = (r, c)
        elif v == "#":
            obs.add((r, c))


def out(coord):
    r, c = coord
    return r < 0 or r >= dim or c < 0 or c >= dim


def next_coord(coord, direct):
    r, c = coord
    if direct == 0:
        return r - 1, c
    if direct == 1:
        return r, c + 1
    if direct == 2:
        return r + 1, c
    return r, c - 1


def uniq_visited(new_obs=None):
    cur_obs = obs.copy()
    if new_obs:
        cur_obs.add(new_obs)

    cur = start
    direct = 0
    visited = set()
    visited_dir = set()
    while True:
        visited.add(cur)
        if (cur, direct) in visited_dir:
            return None
        visited_dir.add((cur, direct))
        n = next_coord(cur, direct)
        if out(n):
            break
        if n in cur_obs:
            direct = (direct + 1) % 4
        else:
            cur = n
    return len(visited)


print(uniq_visited())

count = 0
for r in range(dim):
    for c in range(dim):
        coord = r, c
        if coord not in obs and coord != start:
            res = uniq_visited(coord)
            if res is None:
                count = count + 1
print(count)


