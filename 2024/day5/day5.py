from functools import cmp_to_key

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

sep = lines.index("")
rules = lines[0:sep]
updates = lines[sep + 1:]

rules = set(tuple(int(x) for x in l.split("|")) for l in rules)
updates = [[int(x) for x in l.split(",")] for l in updates]


def ordering(x, y):
    return -1 if (x, y) in rules else 1


def is_correct(update):
    for x, y in rules:
        try:
            ix = update.index(x)
            iy = update.index(y)
        except Exception:
            continue
        if ix > iy:
            return False
    return True


s = 0
for u in updates:
    if is_correct(u):
        s = s + u[len(u) // 2]
print(s)


def fixed_middle(update):
    fixed = sorted(update, key=cmp_to_key(ordering))
    return fixed[len(fixed) // 2]


s = 0
for u in updates:
    if not is_correct(u):
        s = s + fixed_middle(u)
print(s)
