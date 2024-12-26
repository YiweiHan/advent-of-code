from itertools import groupby, product

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

patterns = [list(g) for k, g in groupby(lines, key=bool) if k]


def heights(pattern):
    h = []
    for c in range(5):
        i = 0
        for r in range(7):
            if pattern[r][c] == '#':
                i += 1
        h.append(i)
    return tuple(h)


locks = []
keys = []

for p in patterns:
    h = heights(p)
    if all(x == '#' for x in p[0]):
        locks.append(h)
    else:
        keys.append(h)


def compat(lock, key):
    for l, k in zip(lock, key):
        if l + k > 7:
            return False
    return True


print(sum([compat(lock, key) for lock, key in product(locks, keys)]))
