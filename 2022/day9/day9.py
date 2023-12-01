import re
from math import copysign

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

h = (0, 0)
t = [(0, 0)] * 9
t1_seen = set()
t1_seen.add((0, 0))
t9_seen = set()
t9_seen.add((0, 0))


def h_mov1(dir):
    global h
    h = (h[0] + (1 if dir == "R" else -1 if dir == "L" else 0), h[1] + (1 if dir == "U" else -1 if dir == "D" else 0))


def follow1(target, follower):
    delta_x, delta_y = target[0] - follower[0], target[1] - follower[1]

    if abs(delta_x) < 2 and abs(delta_y) < 2:
        return follower

    mov_x, mov_y = int(copysign(1, delta_x)), int(copysign(1, delta_y))
    if delta_x == 0:
        return follower[0], follower[1] + mov_y
    if delta_y == 0:
        return follower[0] + mov_x, follower[1]

    return follower[0] + mov_x, follower[1] + mov_y


for line in lines:
    dir, dist = re.split(" ", line)
    dist = int(dist)
    for _ in range(dist):
        h_mov1(dir)
        for i in range(len(t)):
            target = h if i == 0 else t[i - 1]
            t[i] = follow1(target, t[i])
        t1_seen.add(t[0])
        t9_seen.add(t[-1])

print(len(t1_seen))
print(len(t9_seen))
