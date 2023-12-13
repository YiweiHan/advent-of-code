from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

grids = [list(i[1]) for i in groupby(lines, lambda i: i != '') if i[0]]


def summarize(grid, diff):
    def compare(grid1, grid2):
        return sum(sum(c1 != c2 for c1, c2 in zip(r1, r2)) for r1, r2 in zip(grid1, grid2)) == diff

    def horizontal_divider(grid):
        for divider in range(1, len(grid)):
            reflect_len = min(divider, len(grid) - divider)
            top = grid[divider - reflect_len:divider]
            bot_reverse = grid[divider:divider + reflect_len][::-1]
            if compare(top, bot_reverse):
                return divider
        return 0

    return horizontal_divider(grid) * 100 + horizontal_divider(list(map(list, zip(*grid))))


# part 1
print(sum(summarize(grid, 0) for grid in grids))

# part 2
print(sum(summarize(grid, 1) for grid in grids))
