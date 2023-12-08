import re
from math import lcm

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dirs = lines.pop(0)
lines.pop(0)

nodes = {}
for line in lines:
    parsed = re.split(r"[\s=(),]+", line)
    nodes[parsed[0]] = (parsed[1], parsed[2])


def traverse(start, end_condition):
    cur = start
    steps = 0
    dirs_i = 0
    while True:
        d = dirs[dirs_i]
        if end_condition(cur):
            return steps
        next_node = nodes[cur]
        cur = next_node[0] if d == "L" else next_node[1]
        steps = steps + 1
        dirs_i = (dirs_i + 1) % len(dirs)


# part 1
print(traverse("AAA", lambda n: n == "ZZZ"))

# part 2
starts = {n for n in nodes.keys() if n.endswith("A")}
print(lcm(*[traverse(s, lambda n: n.endswith("Z")) for s in starts]))
