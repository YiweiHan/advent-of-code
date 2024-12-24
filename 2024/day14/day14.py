import re
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

robots = []
for l in lines:
    px, py, vx, vy = [int(x) for x in re.findall("p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)", l)[0]]
    robots.append((px, py, vx, vy))

rows, cols = 103, 101
m_row, m_col = rows // 2, cols // 2


def advance_robot(x, y, vx, vy):
    return (x + vx) % cols, (y + vy) % rows


def cycle(robots):
    new_robots = []
    for px, py, vx, vy in robots:
        cx, cy = advance_robot(px, py, vx, vy)
        new_robots.append((cx, cy, vx, vy))
    return new_robots


new_robots = robots.copy()
for _ in range(100):
    new_robots = cycle(new_robots)


def quadrants(robots):
    qs = defaultdict(int)
    for px, py, _, _ in robots:
        if py < m_row and px < m_col:
            qs[0] += 1
        if py < m_row and px > m_col:
            qs[1] += 1
        if py > m_row and px < m_col:
            qs[2] += 1
        if py > m_row and px > m_col:
            qs[3] += 1
    return qs[0] * qs[1] * qs[2] * qs[3]


print(quadrants(new_robots))


def check_tree(robots):
    coords_by_y = defaultdict(set)
    for x, y, _, _ in robots:
        coords_by_y[y].add((y, x))

    def longest_continuous(xs):
        longest = 0
        cur_len = 0
        for i, x in enumerate(xs[1:]):
            if xs[i] - xs[i-1] > 1:
                if cur_len > longest:
                    longest = cur_len
                cur_len = 0
            else:
                cur_len += 1
        return longest

    for y, same_line_coords in coords_by_y.items():
        if len(same_line_coords) >= 10:
            xs = sorted(x for y, x in same_line_coords)
            if longest_continuous(xs) > 20:
                return True
    return False


new_robots = robots.copy()
seconds = 0
while not check_tree(new_robots):
    new_robots = cycle(new_robots)
    seconds += 1

print(seconds)
