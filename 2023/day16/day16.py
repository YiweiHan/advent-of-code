from collections import deque

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

rows, cols = len(grid), len(grid[0])

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)


def energize(start, start_dir):
    energized = set()
    seen = set()
    q = deque()

    def append_next(cur, diff):
        n = cur[0] + diff[0], cur[1] + diff[1]
        if 0 <= n[0] < rows and 0 <= n[1] < cols:
            q.append((n, diff))

    q.append((start, start_dir))
    while len(q):
        cur, dir = q.pop()
        if (cur, dir) in seen:
            continue
        energized.add(cur)
        seen.add((cur, dir))

        tile = grid[cur[0]][cur[1]]
        if tile == "." \
                or (tile == "|" and (dir == up or dir == down)) \
                or (tile == "-" and (dir == left or dir == right)):
            append_next(cur, dir)
        elif tile == "|":
            append_next(cur, up)
            append_next(cur, down)
        elif tile == "-":
            append_next(cur, left)
            append_next(cur, right)
        elif tile == "\\":
            if dir == left:
                append_next(cur, up)
            elif dir == right:
                append_next(cur, down)
            elif dir == up:
                append_next(cur, left)
            elif dir == down:
                append_next(cur, right)
        elif tile == "/":
            if dir == left:
                append_next(cur, down)
            elif dir == right:
                append_next(cur, up)
            elif dir == up:
                append_next(cur, right)
            elif dir == down:
                append_next(cur, left)
    return len(energized)


# part 1
print(energize((0, 0), right))

# part 2
starts = []
for r in range(rows):
    starts.append(((r, 0), right))
    starts.append(((r, cols - 1), left))
for c in range(cols):
    starts.append(((0, c), down))
    starts.append(((rows - 1, c), up))
print(max(energize(*s) for s in starts))
