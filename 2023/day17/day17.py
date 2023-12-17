import heapq

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

grid = [[int(x) for x in r] for r in grid]
rows, cols = len(grid), len(grid[0])

start = (0, 0)
target = (rows - 1, cols - 1)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
all_dirs = {up, down, left, right}
next_dirs = {
    up: {up, left, right},
    down: {down, left, right},
    left: {up, down, left},
    right: {up, down, right},
}
heuristic = [[None] * cols for _ in grid]


def make_heuristic(r, c):
    def recurse(r, c):
        if heuristic[r][c] is not None:
            return heuristic[r][c]
        v = grid[r][c]
        if r == rows - 1 and c == cols - 1:
            heuristic[r][c] = v
        elif r == rows - 1:
            heuristic[r][c] = v + recurse(r, c + 1)
        elif c == cols - 1:
            heuristic[r][c] = v + recurse(r + 1, c)
        else:
            heuristic[r][c] = v + min(recurse(r + 1, c), recurse(r, c + 1))
        return heuristic[r][c]
    recurse(r, c)
    for r in range(rows):
        for c in range(cols):
            heuristic[r][c] = heuristic[r][c] - grid[r][c]


make_heuristic(*start)
start_heuristic = heuristic[start[0]][start[1]]


def search(min_straight_count, max_straight_count):
    q = []
    heapq.heappush(q, (start_heuristic, 0, start, 0, right))
    heapq.heappush(q, (start_heuristic, 0, start, 0, down))

    min_heat_losses = {}

    def append_next(cur, dir, prev_dir, heat_loss, straight_count, min_straight_count, max_straight_count):
        if dir == prev_dir and straight_count >= max_straight_count:
            return
        if dir != prev_dir and min_straight_count is not None and straight_count < min_straight_count:
            return
        n = cur[0] + dir[0], cur[1] + dir[1]
        if 0 <= n[0] < rows and 0 <= n[1] < cols:
            new_straight_count = straight_count + 1 if dir == prev_dir else 1
            new_heat_loss = heat_loss + grid[n[0]][n[1]]
            priority = new_heat_loss + heuristic[n[0]][n[1]]
            min_heat_loss = min_heat_losses.get((n, new_straight_count, dir))
            if min_heat_loss is None or new_heat_loss < min_heat_loss:
                min_heat_losses[(n, new_straight_count, dir)] = new_heat_loss
                heapq.heappush(q, (priority, new_heat_loss, n, new_straight_count, dir))

    min_heat_loss = None
    while len(q):
        _, heat_loss, cur_pos, straight_count, dir = heapq.heappop(q)
        if cur_pos == target:
            if min_straight_count is None or straight_count >= min_straight_count:
                if min_heat_loss is None or heat_loss < min_heat_loss:
                    min_heat_loss = heat_loss
            continue
        for next_dir in next_dirs[dir]:
            append_next(cur_pos, next_dir, dir, heat_loss, straight_count, min_straight_count, max_straight_count)
    return min_heat_loss


# part 1
print(search(None, 3))

# part 2
print(search(4, 10))
