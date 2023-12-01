import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

region_dim = 50
code = lines[-1]
lines = lines[:-2]

total_rows = len(lines)
total_cols = max(map(len, lines))

space = [l + "".join([" "] * (total_cols - len(l))) for l in lines]
tokens = list(map(lambda t: int(t) if t != "R" and t != "L" else t, re.findall("\d+|[RL]", code)))


def offset_len(s):
    matches = re.search("[.#]+", s)
    first, last = matches.start(), matches.end() - 1
    return first, last - first + 1


def str_col(col):
    return "".join([space[r][col] for r in range(total_rows)])


def move_1(curr_row, curr_col, facing):
    d_row, d_col = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0),
    }.get(facing)
    return curr_row + d_row, curr_col + d_col


def move_part1(curr_row, curr_col, facing):
    new_row, new_col = move_1(curr_row, curr_col, facing)

    col_offset, visible_row_len = offset_len(space[curr_row])
    row_offset, visible_col_len = offset_len(str_col(curr_col))

    new_row = (new_row - row_offset) % visible_col_len + row_offset
    new_col = (new_col - col_offset) % visible_row_len + col_offset
    return new_row, new_col, facing


def sim(move_func):
    facing = 0
    curr_row = 0
    curr_col = space[0].index(".")

    for t in tokens:
        if type(t) == int:
            for _ in range(t):
                new_row, new_col, new_facing = move_func(curr_row, curr_col, facing)
                if space[new_row][new_col] == "#":
                    break
                curr_row, curr_col, facing = new_row, new_col, new_facing
        else:
            facing = (facing + (1 if t == "R" else -1)) % 4
    return curr_row, curr_col, facing


def password(final_row, final_col, final_facing):
    return 1000 * (final_row + 1) + 4 * (final_col + 1) + final_facing


print(password(*sim(move_part1)))


def move_pt2(curr_row, curr_col, facing):
    new_row, new_col = move_1(curr_row, curr_col, facing)

    if 0 <= new_row < total_rows and 0 <= new_col < total_cols and space[new_row][new_col] != " ":
        return new_row, new_col, facing

    if new_row == total_rows:
        return 0, new_col + 2 * region_dim, facing
    if new_col == total_cols:
        return 3 * region_dim - new_row - 1, 2 * region_dim - 1, 2
    if new_col == region_dim and facing == 0:
        return 3 * region_dim - 1, new_row - 2 * region_dim, 3
    if new_row == region_dim and facing == 1:
        return new_col - region_dim, 2 * region_dim - 1, 2
    if new_row == 3 * region_dim and facing == 1:
        return new_col + 2 * region_dim, region_dim - 1, 2
    if new_row == 2 * region_dim - 1 and facing == 3:
        return new_col + region_dim, region_dim, 0
    if new_row < 0:
        if region_dim <= new_col < 2 * region_dim:
            return new_col + 2 * region_dim, 0, 0
        else:
            return total_rows - 1, new_col - 2 * region_dim, facing
    if new_col < 0:
        if 2 * region_dim <= new_row < 3 * region_dim:
            return 3 * region_dim - new_row - 1, region_dim, 0
        else:
            return 0, new_row - 2 * region_dim, 1
    if new_col == region_dim - 1 and facing == 2:
        if 0 <= new_row < region_dim:
            return 3 * region_dim - new_row - 1, 0, 0
        else:
            return 2 * region_dim, new_row - region_dim, 1
    if new_col == 2 * region_dim and facing == 0:
        if region_dim <= new_row < 2 * region_dim:
            return region_dim - 1, new_row + region_dim, 3
        else:
            return 3 * region_dim - new_row - 1, total_cols - 1, 2


print(password(*sim(move_pt2)))
