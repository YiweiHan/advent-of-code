from itertools import groupby
import re
from sympy import solve, Eq
from sympy.abc import a, b

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

machines = [list(g) for k, g in groupby(lines, key=bool) if k]

ps = []
for m in machines:
    ax, ay = [int(x) for x in re.findall("X\\+([0-9]+), Y\\+([0-9]+)", m[0])[0]]
    bx, by = [int(x) for x in re.findall("X\\+([0-9]+), Y\\+([0-9]+)", m[1])[0]]
    px, py = [int(x) for x in re.findall("X=([0-9]+), Y=([0-9]+)", m[2])[0]]
    ps.append((ax, ay, bx, by, px, py))

adder = 10000000000000


def tokens(add=False):
    s = 0
    for ax, ay, bx, by, px, py in ps:
        if add:
            px, py = px + adder, py + adder
        solved = solve([Eq(ax * a + bx * b, px), Eq(ay * a + by * b, py)], [a, b], dict=True)[0]
        aa, bb = solved[a], solved[b]

        if aa.is_integer and bb.is_integer and aa >= 0 and bb >= 0:
            s += aa * 3 + bb
    return s


print(tokens(False))
print(tokens(True))
