from copy import deepcopy
from math import ceil

with open("input.txt", "r") as f:
    grid = [[*r] for r in f.read().splitlines()]


def get_coords(grid, char, row=None):
    result = set()
    for r in range(len(grid)):
        if row is None or r == row:
            for c in range(len(grid[0])):
                if grid[r][c] == char:
                    result.add((r, c))
    return result


def rotate(grid, n):
    new_grid = deepcopy(grid)
    for _ in range(n % 4):
        new_grid = [list(row) for row in zip(*reversed(new_grid))]
    return new_grid


def move_up(grid):
    new_grid = deepcopy(grid)
    while True:
        moved = False
        for r in range(1, len(grid)):
            rounded = get_coords(new_grid, "O", r)
            for _, c in rounded:
                if new_grid[r - 1][c] == ".":
                    new_grid[r - 1][c] = "O"
                    new_grid[r][c] = "."
                    moved = True
        if not moved:
            break
    return new_grid


def load(grid):
    rounded = get_coords(grid, "O")
    total = 0
    for r, _ in rounded:
        total = total + len(grid) - r
    return total


# part 1
print(load(move_up(grid)))


def move_cycle(grid):
    new_grid = deepcopy(grid)
    for rotations in [0, 1, 2, 3]:
        new_grid = rotate(move_up(rotate(new_grid, rotations)), 4 - rotations)
        # pp(new_grid)
    return new_grid


cycles = 1000000000
loads = []
while True:
    grid = move_cycle(grid)
    loads.append(load(grid))

    for divider in range(ceil(len(loads) / 2.0), len(loads)):
        loop_len = min(divider, len(loads) - divider)
        if loop_len < 5:
            continue
        left = loads[divider - loop_len:divider]
        right = loads[divider:divider + loop_len]
        if left == right:
            prefix_len = divider - loop_len
            # part 2
            print(left[(cycles - prefix_len) % len(left) - 1])
            exit(0)
