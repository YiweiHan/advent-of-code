import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

reps = [[int(x) for x in re.split("\\s+", line)] for line in lines]


def is_safe(rep):
    order = None
    for i in range(len(rep) - 1):
        diff = rep[i + 1] - rep[i]
        abs_diff = abs(diff)
        if abs_diff < 1 or abs_diff > 3:
            return False

        if order is not None and ((order < 0 < diff) or (order > 0 > diff)):
            return False
        order = diff
    return True


safe = 0
for rep in reps:
    safe = safe + is_safe(rep)

print(safe)


def gen_reps(orig_rep):
    reps = []
    for i in range(len(orig_rep)):
        rep = []
        for j in range(len(orig_rep)):
            if i != j:
                rep.append(orig_rep[j])
        reps.append(rep)
    return reps


safe2 = 0
for rep in reps:
    v = is_safe(rep)
    if v:
        safe2 = safe2 + 1
    else:
        new_reps = gen_reps(rep)
        for r in new_reps:
            if is_safe(r):
                safe2 = safe2 + 1
                break

print(safe2)


