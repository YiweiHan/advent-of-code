with open("input.txt", "r") as f:
    line = f.read().splitlines()[0]

pairs = [tuple([int(x) for x in p.split("-")]) for p in line.split(",")]


def find_reps_2(a, b):
    ids = set()
    for x in range(a, b + 1):
        if len(str(x)) % 2 != 0:
            continue
        px = str(x)[0:len(str(x)) // 2]
        v = int(px + px)
        if a <= v <= b:
            ids.add(v)
    return ids


def find_reps_x(a, b):
    ids = set()
    for x in range(a, b + 1):
        for pl in range(1, len(str(x)) + 1):
            if len(str(x)) % pl != 0:
                continue
            px = str(x)[0:pl]
            for rep in range(2, len(str(b)) + 1):
                v = int(px * rep)
                if a <= v <= b:
                    ids.add(v)
    return ids


s = 0
s2 = 0
for a, b in pairs:
    s += sum(find_reps_2(a, b))
    s2 += sum(find_reps_x(a, b))

print(s)
print(s2)