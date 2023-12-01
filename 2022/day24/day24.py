import sys

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

rows, cols = len(lines), len(lines[0])

start = (0, 1)
goal = (rows - 1, lines[-1].index("."))

wind_right = set()
wind_left = set()
wind_up = set()
wind_down = set()

wind_map = {
    ">": wind_right,
    "<": wind_left,
    "^": wind_up,
    "v": wind_down,
}

for r in range(rows):
    for c in range(cols):
        char = lines[r][c]
        if char != "." and char != "#":
            wind_map[char].add((r, c))


def predict_winds(wind_right, wind_left, wind_up, wind_down):
    next_wind_right = set(map(lambda w: (w[0], w[1] + 1 if w[1] + 1 != cols - 1 else 1), wind_right))
    next_wind_left = set(map(lambda w: (w[0], w[1] - 1 if w[1] - 1 != 0 else cols - 2), wind_left))
    next_wind_up = set(map(lambda w: (w[0] - 1 if w[0] - 1 != 0 else rows - 2, w[1]), wind_up))
    next_wind_down = set(map(lambda w: (w[0] + 1 if w[0] + 1 != rows - 1 else 1, w[1]), wind_down))
    return next_wind_right, next_wind_left, next_wind_up, next_wind_down


total_wind_states = (rows - 2) * (cols - 2)
wind_states = {}

for i in range(total_wind_states):
    wind_states[i] = set()
    wind_states[i] |= wind_right
    wind_states[i] |= wind_left
    wind_states[i] |= wind_up
    wind_states[i] |= wind_down
    wind_right, wind_left, wind_up, wind_down = predict_winds(wind_right, wind_left, wind_up, wind_down)


def next_possible_moves(p, wind_state):
    def movable(p):
        if p == start or p == goal:
            return True
        if p[0] < 1 or p[1] < 1 or p[0] >= rows - 1 or p[1] >= cols - 1:
            return False
        return p not in wind_state

    deltas = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]
    return set(filter(movable, [(p[0] + d[0], p[1] + d[1]) for d in deltas]))


def manhattan(p, goal_p):
    return sum((abs(p[0] - goal_p[0]), abs(p[1] - goal_p[1])))


def sim(start_p, goal_p, wind_state_offset=0):
    seen_states = {}

    s = [(start_p, 0)]
    shortest = sys.maxsize

    while s:
        p, minutes = s.pop()

        if p == goal_p:
            shortest = min(shortest, minutes)
            continue

        if minutes + manhattan(p, goal_p) >= shortest:
            continue

        wind_state_index = (minutes + wind_state_offset) % total_wind_states
        if (p, wind_state_index) in seen_states:
            prev_minutes = seen_states[(p, wind_state_index)]
            if minutes >= prev_minutes:
                continue
        seen_states[(p, wind_state_index)] = minutes

        next_ps = next_possible_moves(p, wind_states[(wind_state_index + 1) % total_wind_states])
        next_states = [(p, minutes + 1) for p in next_ps]

        s.extend(sorted(next_states, key=lambda st: manhattan(st[0], goal_p), reverse=True))

    return shortest


# part 1
minutes_to_goal1 = sim(start, goal)
print(minutes_to_goal1)

# part 2
minutes_to_start1 = sim(goal, start, minutes_to_goal1)
minutes_to_goal2 = sim(start, goal, minutes_to_goal1 + minutes_to_start1)
print(minutes_to_goal1 + minutes_to_start1 + minutes_to_goal2)

