with open("input.txt", "r") as f:
    grid = f.read().splitlines()


grid = [[c for c in r] for r in grid]
rows = len(grid)
cols = len(grid[0])


def find_neighbour_rolls(g, r, c):
    pts = [
        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
        (r, c - 1), (r, c + 1),
        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)
    ]
    ns = set()
    for r, c in pts:
        if 0 <= r < rows and 0 <= c < cols and g[r][c] == "@":
            ns.add((r, c))
    return ns


def find_removable_rolls(g):
    rr = set()
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == "@":
                ns = find_neighbour_rolls(g, r, c)
                if len(ns) < 4:
                    rr.add((r, c))
    return rr


print(len(find_removable_rolls(grid)))

removed = set()
while True:
    rm = find_removable_rolls(grid)
    if len(rm) == 0:
        break
    for r, c in rm:
        grid[r][c] = "."
    removed.update(rm)

print(len(removed))
