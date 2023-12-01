from itertools import groupby
import re
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

start_stack_lines, instructions = [list(group) for k, group in groupby(lines, bool) if k]


def build_stack(start_lines):
    v = defaultdict(list)
    for line in list(reversed(start_lines[0:len(start_lines) - 1])):
        for i in range(9):
            item = line[i * 4 + 1]
            if item != " ":
                v[i + 1].append(item)
    return v


# part 1
def move_one_at_a_time(state, num, src, dst):
    for _ in range(num):
        state[dst].append(state[src].pop())


state = build_stack(start_stack_lines)
for ins in instructions:
    (num, src, dst) = map(int, filter(None, re.split("[a-z ]+", ins)))
    move_one_at_a_time(state, num, src, dst)

print("".join(map(lambda col: col[len(col) - 1], state.values())))


# part 2
def move_num_at_a_time(state, num, src, dst):
    buffer = []
    for _ in range(num):
        buffer.append(state[src].pop())
    state[dst].extend(reversed(buffer))


state = build_stack(start_stack_lines)
for ins in instructions:
    (num, src, dst) = map(int, filter(None, re.split("[a-z ]+", ins)))
    move_num_at_a_time(state, num, src, dst)

print("".join(map(lambda col: col[len(col) - 1], state.values())))
