import numpy as np

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


space = np.zeros(shape=(len(lines), len(lines[0])), dtype=np.int32)

for i, line in enumerate(lines):
    space[i, :] = list(map(int, [*line]))

rows, cols = space.shape


def is_visible(val, row_left, row_right, col_top, col_bot):
    return all(row_left < val) or all(row_right < val) or all(col_top < val) or all(col_bot < val)


def score(val, row_left, row_right, col_top, col_bot):
    def dist(segment):
        idx = next((i for i, h in enumerate(segment) if h >= val), None)
        return idx + 1 if idx is not None else len(segment)

    dist_left = dist(list(reversed(row_left)))
    dist_right = dist(row_right)
    dist_top = dist(list(reversed(col_top)))
    dist_bot = dist(col_bot)
    return dist_left * dist_right * dist_top * dist_bot


visible = 0
scores = []
for i in range(rows):
    row = space[i, :]
    for j in range(cols):
        val = space[i, j]
        row_left = space[i, 0:j]
        row_right = space[i, j + 1:rows]
        col_top = space[0:i, j]
        col_bot = space[i + 1:cols, j]
        visible += is_visible(val, row_left, row_right, col_top, col_bot)
        scores.append(score(val, row_left, row_right, col_top, col_bot))

print(visible)
print(max(scores))
