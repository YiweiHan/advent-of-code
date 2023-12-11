from itertools import combinations


with open("input.txt", "r") as f:
    grid = f.read().splitlines()

rows, cols = len(grid), len(grid[0])

empty_rows = set()
for r in range(rows):
    if all([x == "." for x in grid[r]]):
        empty_rows.add(r)

empty_cols = set()
for c in range(cols):
    if all([grid[r][c] == "." for r in range(rows)]):
        empty_cols.add(c)

galaxies = set()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "#":
            galaxies.add((r, c))


def shortest_path_len(start_p, target_p, empty_multiplier):
    r_range = (start_p[0], target_p[0]) if start_p[0] < target_p[0] else (target_p[0], start_p[0])
    c_range = (start_p[1], target_p[1]) if start_p[1] < target_p[1] else (target_p[1], start_p[1])

    empty_crossing_count = 0
    for r in empty_rows:
        if r_range[0] < r < r_range[1]:
            empty_crossing_count = empty_crossing_count + 1
    for c in empty_cols:
        if c_range[0] < c < c_range[1]:
            empty_crossing_count = empty_crossing_count + 1

    return abs(target_p[0] - start_p[0]) + abs(target_p[1] - start_p[1]) + (empty_multiplier - 1) * empty_crossing_count


def sum_shortest_distances(empty_multiplier):
    total = 0
    for a, b in combinations(galaxies, 2):
        total = total + shortest_path_len(a, b, empty_multiplier)
    print(total)


# part 1
sum_shortest_distances(2)

# part 2
sum_shortest_distances(1000000)
