from functools import cache
from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

patterns, designs = [list(g) for k, g in groupby(lines, key=bool) if k]
patterns = set(patterns[0].split(", "))


def next_patterns(rem):
    return [p for p in patterns if rem.startswith(p)]


@cache
def search2(remaining, cur):
    if remaining == "":
        return 1
    ns = next_patterns(remaining)
    s = 0
    for n in ns:
        s += search2(remaining[len(n):], cur + n)
    return s


s = 0
s2 = 0
for d in designs:
    ways = search2(d, "")
    s += ways > 0
    s2 += ways

print(s)
print(s2)
