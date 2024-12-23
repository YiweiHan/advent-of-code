from collections import defaultdict
from functools import cache
from copy import deepcopy

with open("input.txt", "r") as f:
    line = f.read().splitlines()[0]

stones = [int(x) for x in line.split(" ")]


@cache
def blink(n):
    str_n = str(n)
    if n == 0:
        return [1]
    elif len(str_n) % 2 == 0:
        l = int(str_n[0:len(str_n) // 2])
        r = int(str_n[len(str_n) // 2:])
        return [l, r]
    else:
        return [n * 2024]


def next_cycle(stones_freq):
    new_stones_freq = defaultdict(int)
    for n, freq in stones_freq.items():
        new_stones = blink(n)
        for ns in new_stones:
            new_stones_freq[ns] = new_stones_freq[ns] + freq
    return new_stones_freq


stones_freq = defaultdict(int)
for n in stones:
    stones_freq[n] = stones_freq[n] + 1


def cycle(cycles):
    new_stones_freq = deepcopy(stones_freq)
    for i in range(cycles):
        new_stones_freq = next_cycle(new_stones_freq)
    return sum(new_stones_freq.values())


print(cycle(25))
print(cycle(75))
