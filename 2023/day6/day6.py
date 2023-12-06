import re
from functools import reduce

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

times = [int(x) for x in re.split(r"\s+", lines[0])[1:]]
distances = [int(x) for x in re.split(r"\s+", lines[1])[1:]]


def get_wins_per_race(times, distances):
    wins_per_race = []
    for t, d in zip(times, distances):
        wins = 0
        for hold_ms in range(1, t):
            time_left = t - hold_ms
            dist = hold_ms * time_left
            if dist > d:
                wins = wins + 1
        wins_per_race.append(wins)
    return wins_per_race


# part 1
print(reduce(lambda x, y: x * y, get_wins_per_race(times, distances)))

# part 2
single_time = int("".join([str(x) for x in times]))
single_distance = int("".join([str(x) for x in distances]))
print(get_wins_per_race([single_time], [single_distance])[0])



