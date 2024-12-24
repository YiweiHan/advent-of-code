from itertools import groupby
import numpy as np

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

lines, dirs = [list(g) for k, g in groupby(lines, key=bool) if k]
dirs = "".join(dirs)
grid = np.array([[x for x in line] for line in lines])


def get_pos(grid):
    p = np.where(grid == '@')
    return int(p[0][0]), int(p[1][0])


def next_pos(p, d):
    vec = {
        '>': (0, 1),
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0),
    }[d]
    return p[0] + vec[0], p[1] + vec[1]


def push(grid, src_p, d, move):
    n = next_pos(src_p, d)
    v = grid[n]
    if v == '#':
        return False
    if v == '.':
        if move:
            grid[n] = grid[src_p]
        return True
    if v == 'O' or ((d == '<' or d == '>') and (v == '[' or v == ']')):
        next_push = push(grid, n, d, move)
        if next_push:
            if move:
                grid[n] = grid[src_p]
            return True
        return False
    if d == '^' or d == 'v':
        next_push = push(grid, n, d, move)
        if v == '[':
            n2 = (n[0], n[1] + 1)
            next_push2 = push(grid, n2, d, move)
        elif v == ']':
            n2 = (n[0], n[1] - 1)
            next_push2 = push(grid, n2, d, move)
        else:
            return False
        if next_push and next_push2:
            if move:
                grid[n] = grid[src_p]
                grid[n2] = '.'
            return True
    return False


def gps(grid, c):
    obs_coords = np.where(grid == c)
    return sum(100 * obs_coords[0]) + sum(obs_coords[1])


def cycle(grid):
    for d in dirs:
        p = get_pos(grid)
        can_move = push(grid, p, d, False)
        if can_move:
            push(grid, p, d, True)
            new_pos = next_pos(p, d)
            grid[p] = '.'
            grid[new_pos] = '@'


cycle(grid)
print(gps(grid, 'O'))

wide_map = []
for line in lines:
    wide_row = []
    for c in line:
        if c == '#' or c == '.':
            wide_row.extend([c, c])
        if c == '@':
            wide_row.extend([c, '.'])
        if c == 'O':
            wide_row.extend(['[', ']'])
    wide_map.append(wide_row)

grid = np.array(wide_map)

cycle(grid)
print(gps(grid, '['))
