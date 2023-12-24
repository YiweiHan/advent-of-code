from collections import defaultdict, deque

with open("input.txt", "r") as f:
    grid = f.read().splitlines()

rows, cols = len(grid), len(grid[0])
start = (0, 1)
end = (rows - 1, cols - 2)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
dir_map = {
    ">": right,
    "<": left,
    "^": up,
    "v": down,
}


def neighbours(p):
    return [((p[0] + dir[0], p[1] + dir[1]), dir) for dir in dir_map.values()]


def is_fork(p):
    return grid[p[0]][p[1]] == "." and sum(grid[n[0][0]][n[0][1]] in dir_map for n in neighbours(p)) >= 2


def next_pos(p, directed):
    def direction_valid(p, dir):
        tile = grid[p[0]][p[1]]
        return dir_map[tile] == dir if tile in dir_map else True

    nexts = list(filter(lambda n: 0 <= n[0][0] < rows and 0 <= n[0][1] < cols and grid[n[0][0]][n[0][1]] != "#", neighbours(p)))
    if directed:
        nexts = list(filter(lambda n: direction_valid(n[0], n[1]), nexts))
    return [n[0] for n in nexts]


nodes = {start, end}
for r in range(1, rows - 1):
    for c in range(1, cols - 1):
        if is_fork((r, c)):
            nodes.add((r, c))


def adjacency(directed):
    steps_from_to = defaultdict(dict)

    for start_node in nodes:
        q = deque()
        q.append((start_node, None, start_node, 0))
        while len(q):
            cur, prev_pos, prev_node, prev_node_dist = q.popleft()

            if cur in nodes and cur != start_node:
                steps_from_to[prev_node][cur] = prev_node_dist
                continue

            new_node = prev_node
            new_node_dist = prev_node_dist + 1
            q.extend([(n, cur, new_node, new_node_dist) for n in next_pos(cur, directed) if n != prev_pos])
    return steps_from_to


def find_max_steps(directed):
    steps_from_to = adjacency(directed)

    max_steps = 0
    q = deque()
    q.append((start, set(), 0))
    while len(q):
        cur, nodes_visited, steps_taken = q.pop()

        if cur == end and steps_taken > max_steps:
            max_steps = steps_taken
            continue

        new_nodes_visited = nodes_visited.union({cur})
        q.extend([(next_node, new_nodes_visited, steps_taken + steps) for next_node, steps in steps_from_to[cur].items() if next_node not in nodes_visited])
    return max_steps


# part 1
print(find_max_steps(True))

# part 2
print(find_max_steps(False))

