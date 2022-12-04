import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


# part 1
def part1(line):
    (x1, x2, y1, y2) = map(lambda v: int(v), re.split("[,-]", line))
    return (x1 <= y1 and x2 >= y2) or (y1 <= x1 and y2 >= x2)


print(sum(map(part1, lines)))


# part 2
def part2(line):
    (x1, x2, y1, y2) = map(lambda v: int(v), re.split("[,-]", line))
    return x1 <= y2 and y1 <= x2


print(sum(map(part2, lines)))
