from collections import deque


with open("input.txt", "r") as f:
    grid = f.read().splitlines()

rows = len(grid)
cols = len(grid[0])

start_r = start_c = None
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "S":
            start_r, start_c = r, c

bends = {"7", "F", "L", "J"}
connected_north_tiles = {"|", "7", "F"}
connected_south_tiles = {"|", "L", "J"}
connected_east_tiles = {"-", "J", "7"}
connected_west_tiles = {"-", "L", "F"}

next_pos_diff_by_tile = {
    "|": {(-1, 0), (1, 0)},
    "-": {(0, -1), (0, 1)},
    "7": {(1, 0), (0, -1)},
    "J": {(0, -1), (-1, 0)},
    "L": {(0, 1), (-1, 0)},
    "F": {(0, 1), (1, 0)},
}

step_one_coords = [
    (start_r - 1, start_c) if grid[start_r - 1][start_c] in connected_north_tiles else None,
    (start_r + 1, start_c) if grid[start_r + 1][start_c] in connected_south_tiles else None,
    (start_r, start_c + 1) if grid[start_r][start_c + 1] in connected_east_tiles else None,
    (start_r, start_c - 1) if grid[start_r][start_c - 1] in connected_west_tiles else None,
]
step_one_coords_connected = [p is not None for p in step_one_coords]


step_one_coords = list(filter(lambda p: p is not None and 0 <= p[0] < rows and 0 <= p[1] < cols, step_one_coords))


s_tile = None
if step_one_coords_connected[0]:
    if step_one_coords_connected[1]:
        s_tile = '|'
    elif step_one_coords_connected[2]:
        s_tile = 'L'
    else:
        s_tile = 'J'
elif step_one_coords_connected[2]:
    if step_one_coords_connected[3]:
        s_tile = '-'
    elif step_one_coords_connected[1]:
        s_tile = 'F'
else:
    s_tile = '7'

amended_grid = []
for row in grid:
    amended_grid.append(row.replace("S", s_tile))

grid = amended_grid


def find_loop():
    def get_next_tile(r, c, path):
        diffs = next_pos_diff_by_tile[grid[r][c]]
        cur_pos = path[-1][0:2]
        return list(filter(lambda p: cur_pos != p, {(r + dr, c + dc) for dr, dc in diffs}))[0]

    q = deque()
    for s in step_one_coords:
        q.append((s[0], s[1], [(start_r, start_c)]))
    seen_pos = {(start_r, start_c): []}

    while len(q):
        r, c, path = q.popleft()
        if (r, c) in seen_pos:
            return path, (r, c), seen_pos[(r, c)]
        seen_pos[(r, c)] = path
        next_pos = get_next_tile(r, c, path)
        new_path = path[:] + [(r, c)]
        q.append((next_pos[0], next_pos[1], new_path))


path, (last_r, last_c), alt_path = find_loop()
# part 1
print(len(path))

# part 2
full_path_coords = set(path + alt_path + [(last_r, last_c)])

total_inside = 0
for r in range(rows):
    is_inside = False
    last_event = None
    for c in range(cols):
        if (r, c) in full_path_coords:
            tile = grid[r][c]
            if tile == "-":
                continue
            elif tile == "|":
                is_inside = not is_inside
                last_event = "|"
            elif tile == "J":
                if last_event == "F":
                    is_inside = not is_inside
                last_event = "J"
            elif tile == "7":
                if last_event == "L":
                    is_inside = not is_inside
                last_event = "7"
            else:
                last_event = tile
        else:
            total_inside = total_inside + is_inside

print(total_inside)
