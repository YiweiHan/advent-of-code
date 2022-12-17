import re
from collections import defaultdict
from itertools import combinations

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

valves = {}
pressure_valves = set()
for line in lines:
    _, valve, _, _, _, rate, _, _, _, _, leads = re.split("[ ;,=]+", line, maxsplit=10)
    rate = int(rate)
    leads = re.split("[, ]+", leads)

    valves[valve] = (rate, leads)
    if rate > 0:
        pressure_valves.add(valve)

min_dists_between_valves = defaultdict(lambda: defaultdict(int))


def bfs_min_dists(src_v):
    q = [(src_v, 0)]
    ex = set()
    while q:
        v, dist = q.pop(0)

        if v in ex:
            continue

        ex.add(v)

        if v != src_v:
            min_dists_between_valves[v][src_v] = dist
            min_dists_between_valves[src_v][v] = dist

        for next_v in valves[v][1]:
            q.append((next_v, dist + 1))


for v in valves.keys():
    bfs_min_dists(v)


# state = (valve, map of opened valve -> minutes remaining when opened, remaining minutes)
part1_start_state = ("AA", {}, 30)
part2_start_state = ("AA", {}, 26)


def bfs(start_state, target_pressure_valves):
    seen_states = set()

    q = [start_state]
    max_released = 0

    while q:
        valve, valves_released_time_remaining, remaining_minutes = q.pop(0)

        if remaining_minutes <= 0 or len(target_pressure_valves - valves_released_time_remaining.keys()) == 0:
            max_released = max(max_released, sum([(time_remaining - 1) * valves[v][0] for v, time_remaining in valves_released_time_remaining.items()]))
            continue

        hashed_state = (valve, frozenset([(v, time_remaining) for v, time_remaining in valves_released_time_remaining.items()]))
        if hashed_state in seen_states:
            continue
        seen_states.add(hashed_state)

        if valve in target_pressure_valves and valve not in valves_released_time_remaining:
            new_valves_released_time_remaining = valves_released_time_remaining.copy()
            new_valves_released_time_remaining[valve] = remaining_minutes
            q.append((valve, new_valves_released_time_remaining, remaining_minutes - 1))
        else:
            for next_valve, dist in [(v, dist) for v, dist in min_dists_between_valves[valve].items() if v in target_pressure_valves and v not in valves_released_time_remaining]:
                q.append((next_valve, valves_released_time_remaining, remaining_minutes - dist))
    return max_released


# part 1
print(bfs(part1_start_state, pressure_valves))


# part 2
max_released = 0
a1_targets_seen = set()
for i in range(1, len(pressure_valves)):
    for a1_targets in map(set, combinations(pressure_valves, i)):
        a2_targets = pressure_valves - a1_targets

        if frozenset(a2_targets) in a1_targets_seen:
            continue
        a1_targets_seen.add(frozenset(a1_targets))

        max_released = max(max_released, sum([bfs(part2_start_state, a1_targets), bfs(part2_start_state, a2_targets)]))
print(max_released)
