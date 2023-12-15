import re
from collections import defaultdict

with open("input.txt", "r") as f:
    line = f.read().splitlines()[0]

steps = re.split(r",", line)


def hash_value(string):
    val = 0
    for c in string:
        val = ((val + ord(c)) * 17) % 256
    return val


# part 1
print(sum(hash_value(s) for s in steps))


boxes = defaultdict(list)

def lens_idx(lenses, label):
    for i, lens in enumerate(lenses):
        if lens[0] == label:
            return i


def insert(label, fl):
    box = hash_value(label)
    lenses = boxes[box]
    idx = lens_idx(lenses, label)
    if idx is None:
        lenses.append((label, fl))
    else:
        lenses[idx] = (label, fl)


def delete(label):
    box = hash_value(label)
    lenses = boxes[box]
    idx = lens_idx(lenses, label)
    if idx is not None:
        lenses.pop(idx)


for step in steps:
    if "=" in step:
        label, fl = step.split("=")
        insert(label, fl)
    else:
        label = step.split("-")[0]
        delete(label)

total = 0
for box, lenses in boxes.items():
    for i, lens in enumerate(lenses):
        total = total + (box + 1) * (i + 1) * int(lens[1])

# part 2
print(total)
