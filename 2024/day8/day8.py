from itertools import permutations
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)

antennas = defaultdict(set)
for r in range(dim):
    for c in range(dim):
        v = lines[r][c]
        if v != '.':
            antennas[v].add((r, c))


def out(coord):
    r, c = coord
    return r < 0 or r >= dim or c < 0 or c >= dim


def anode(coord1, coord2, extend):
    (r1, c1), (r2, c2) = coord1, coord2
    rel = r2 - r1, c2 - c1
    ans = []
    if extend:
        for f in range(dim):
            ans.append((r1 - f * rel[0], c1 - f * rel[1]))
    else:
        ans.append((r1 - rel[0], c1 - rel[1]))
    return ans


def count_anodes(extend):
    anodes = set()
    for a, coords in antennas.items():
        pairs = permutations(coords, 2)
        for coord1, coord2 in pairs:
            ans = anode(coord1, coord2, extend)
            for an in ans:
                if not out(an):
                    anodes.add(an)
    return len(anodes)


print(count_anodes(False))
print(count_anodes(True))
