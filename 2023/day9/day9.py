import re
from itertools import pairwise

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

histories = [[int(x) for x in re.split(r"\s+", line)] for line in lines]


def predict_next(history):
    diffs = [history]
    next_seq = history
    while True:
        next_seq = [b - a for a, b in pairwise(next_seq)]
        diffs.append(next_seq)
        if all([x == 0 for x in next_seq]):
            break
    reverse_diffs = diffs[::-1]

    last_diff = 0
    for d in reverse_diffs:
        d.append(d[-1] + last_diff)
        last_diff = d[-1]
    return reverse_diffs[-1][-1]


# part 1
print(sum([predict_next(h) for h in histories]))

# part 2
for h in histories:
    h.reverse()
print(sum([predict_next(h) for h in histories]))
