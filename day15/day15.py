import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

readings = list(map(lambda l: eval(re.sub(":", ",", re.sub("[a-zA-Z =]+", "", l))), lines))


def manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


stats = [((r[0], r[1]), (r[2], r[3]), manhattan(*r)) for r in readings]


def merge_ranges(rs):
    sorted_rs = sorted([list(r) for r in rs], key=lambda r: r[0])
    merged = [sorted_rs[0]]
    for curr in sorted_rs:
        last = merged[-1]
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
        else:
            merged.append(curr)
    return merged


def x_range_coverage(y):
    x_ranges = []
    for (sensor_x, sensor_y), _, dist in stats:
        if (sensor_y - dist) <= y <= (sensor_y + dist):
            dy = abs(sensor_y - y)
            dx = dist - dy
            x_ranges.append((sensor_x - dx, sensor_x + dx))
    return merge_ranges(x_ranges)


# part 1
part1_y = 2000000
x_ranges = x_range_coverage(part1_y)
beacons = set([p[1] for p in stats])
beacons_xs_at_y = set(map(lambda b: b[0], filter(lambda b: b[1] == part1_y, beacons)))
no_beacon_count = sum(map(lambda r: r[1] - r[0] + 1, x_ranges))
for r in x_ranges:
    for bx in beacons_xs_at_y:
        if r[0] <= bx <= r[1]:
            no_beacon_count -= 1
print(no_beacon_count)


# part 2
for y in range(4000001):
    x_ranges = x_range_coverage(y)
    if len(x_ranges) > 1:
        print((x_ranges[0][1] + 1) * 4000000 + y)
        break
