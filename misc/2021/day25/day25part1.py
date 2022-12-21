import numpy as np

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

rows = len(lines)
cols = len(lines[0])
space = np.empty(shape=(rows, cols), dtype=np.uint8)
for r in range(rows):
    for c in range(cols):
        pt = lines[r][c]
        space[r][c] = 0 if pt == "." else 1 if pt == ">" else 2

steps = 0
while True:
    steps += 1
    moved = False

    easts = np.argwhere(space == 1)
    new_space = space.copy()
    for r, c in easts:
        target_c = (c + 1) % cols
        if space[r][target_c] == 0:
            new_space[r][c], new_space[r][target_c] = new_space[r][target_c], new_space[r][c]
            moved = True
    space = new_space.copy()

    souths = np.argwhere(space == 2)
    for r, c in souths:
        target_r = (r + 1) % rows
        if space[target_r][c] == 0:
            new_space[r][c], new_space[target_r][c] = new_space[target_r][c], new_space[r][c]
            moved = True
    space = new_space.copy()

    if not moved:
        break

print(steps)
