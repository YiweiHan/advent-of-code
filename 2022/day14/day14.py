import re
from itertools import pairwise

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

paths = list(map(lambda l: list(map(eval, re.split(" -> ", l))), lines))

sand_start = (500, 0)

paths_max_y = max([p[1] for path in paths for p in path])
floor_y = paths_max_y + 2

on_path_cache = {}


def is_on_path(x, y):
    if (x, y) in on_path_cache:
        return on_path_cache[(x, y)]
    for p in paths:
        for (p1_x, p1_y), (p2_x, p2_y) in pairwise(p):
            if (p1_x == p2_x == x and (p1_y <= y <= p2_y or p2_y <= y <= p1_y)) or (p1_y == p2_y == y and (p1_x <= x <= p2_x or p2_x <= x <= p1_x)) or y == floor_y:
                on_path_cache[(x, y)] = True
                return True
    on_path_cache[(x, y)] = False
    return False


def run(max_y):
    sand_occupied = set()

    def is_occupied(x, y):
        return is_on_path(x, y) or (x, y) in sand_occupied

    def fall():
        sand_x, sand_y = sand_start

        if is_occupied(sand_x, sand_y):
            return None

        while True:
            if sand_y == max_y:
                return None
            if not is_occupied(sand_x, sand_y + 1):
                sand_y += 1
                continue
            if not is_occupied(sand_x - 1, sand_y + 1):
                sand_x -= 1
                sand_y += 1
                continue
            if not is_occupied(sand_x + 1, sand_y + 1):
                sand_x += 1
                sand_y += 1
                continue
            return sand_x, sand_y

    while True:
        rest = fall()
        if rest is None:
            break

        sand_occupied.add(rest)
    return len(sand_occupied)


print(run(paths_max_y))
print(run(floor_y))
