with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# x, y
start_part_1 = None
starts_part_2 = []
end = None

space = []
for row, line in enumerate(lines):
    space.append(line.replace("S", "a").replace("E", "z"))
    for col, c in enumerate(line):
        if c == "S":
            start_part_1 = (col, row)
        if c == "E":
            end = (col, row)
        if c == "a" or c == "S":
            starts_part_2.append((col, row))

rows, cols = len(space), len(space[0])


def bfs(start):
    def get_next_positions(x, y):
        def elevation(x, y):
            return ord(space[y][x])

        pos = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return list(filter(lambda p: 0 <= p[0] < cols and 0 <= p[1] < rows and elevation(p[0], p[1]) - elevation(x, y) <= 1, pos))

    expand_q = [(start, 0)]
    trail_steps = set()
    expanded = set()
    while len(expand_q) > 0:
        curr, steps_so_far = expand_q.pop(0)
        if curr in expanded:
            continue

        expanded.add(curr)

        if curr == end:
            trail_steps.add(steps_so_far)
            continue

        next_positions = get_next_positions(curr[0], curr[1])
        expand_q.extend([(e, steps_so_far + 1) for e in next_positions])
    return cols * rows if len(trail_steps) == 0 else min(trail_steps)


print(bfs(start_part_1))
print(min(map(bfs, starts_part_2)))
