import re
from itertools import product, permutations

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

lava_cubes = {tuple(map(int, re.split(",", line))) for line in lines}


def total_surface_area(cubes):
    surface_area = len(cubes) * 6
    for (x1, y1, z1), (x2, y2, z2) in permutations(cubes, 2):
        surface_area -= x1 == x2 and y1 == y2 and abs(z1 - z2) == 1
        surface_area -= y1 == y2 and z1 == z2 and abs(x1 - x2) == 1
        surface_area -= z1 == z2 and x1 == x2 and abs(y1 - y2) == 1
    return surface_area


surface_area = total_surface_area(lava_cubes)
print(surface_area)

x_max = max([x for x, _, _ in lava_cubes])
y_max = max([y for _, y, _ in lava_cubes])
z_max = max([z for _, _, z in lava_cubes])


def bfs_outside(start):
    def next_pts(x, y, z):
        pts = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
        return list(filter(lambda p: 0 <= p[0] <= x_max and 0 <= p[1] <= y_max and 0 <= p[2] <= z_max, pts))

    visited = set()
    q = [start]

    while q:
        p = q.pop(0)
        if p in visited or p in lava_cubes:
            continue
        visited.add(p)
        q.extend(next_pts(*p))
    return visited


all_pts = {(x, y, z) for x, y, z in product(range(x_max + 1), range(y_max + 1), range(z_max + 1))}
outside_pts = bfs_outside((0, 0, 0))
inside_pts = all_pts - outside_pts - lava_cubes

print(surface_area - total_surface_area(inside_pts))
