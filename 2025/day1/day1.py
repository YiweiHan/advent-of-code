with open("input.txt", "r") as f:
    lines = f.read().splitlines()

p = 50
c = 0
c2 = 0

for line in lines:
    delta = (-1 if line[0] == "L" else 1) * int(line[1:])
    p2 = (p + delta)
    q, r = divmod(p2, 100)
    if r == 0:
        c += 1
    c2d = 0
    if q > 0:
        c2d = q
    elif q == 0 and r == 0:
        c2d += 1
    elif q < 0:
        q2, _ = divmod(abs(p2), 100)
        c2d = q2
        if p > 0:
            c2d += 1
    c2 += c2d
    p = r
print(c)
print(c2)
