import re
from itertools import product, combinations

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

hails = []
for line in lines:
    nums = tuple(int(x) for x in re.split(r"[, @]+", line))
    hails.append(((nums[0:3]), (nums[3:])))


def cartesian(hail):
    p1, v = hail
    p2 = tuple(p0_dim + v_dim for p0_dim, v_dim in zip(p1, v))
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = -p1[0] * m + p1[1]
    return m, b


def sim_collisions(hails, exact):
    collisions = []
    for h1, h2 in combinations(hails, 2):
        try:
            m1, b1 = cartesian(h1)
            m2, b2 = cartesian(h2)
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
            ts = [(x - h[0][0]) / h[1][0] for h in [h1, h2]]
            t_valid = all(td >= 0 for td in ts)
            if exact:
                if not t_valid:
                    return
                zs = [h[0][2] + t * h[1][2] for h, t in zip([h1, h2], ts)]
                if zs[0] == zs[1]:
                    if (x, y, zs[0]) in collisions:
                        return x, y, zs[0]
                    collisions.append((x, y, zs[0]))
            elif t_valid:
                collisions.append((x, y))
        except ZeroDivisionError:
            pass
    if not exact:
        return collisions


# part 1
test_range = (200000000000000, 400000000000000)
collisions = sim_collisions(hails, False)
print(sum(test_range[0] <= x <= test_range[1] and test_range[0] <= y <= test_range[1] for x, y in collisions))


# part 2
search_abs_max = 500
search_x = set(range(-search_abs_max, search_abs_max))
search_y = set(range(-search_abs_max, search_abs_max))
search_z = set(range(-search_abs_max, search_abs_max))
search_ranges = [search_x, search_y, search_z]

for h1, h2 in combinations(hails, 2):
    for i in range(3):
        if h1[0][i] > h2[0][i] and h1[1][i] > h2[1][i]:
            search_ranges[i] = search_ranges[i] - set(range(h2[1][i], h1[1][i]))

for v_rel in product(*search_ranges):
    new_hails = [(p, tuple(v_d - v_rel_d for v_d, v_rel_d in zip(v, v_rel))) for p, v in hails]
    collision = sim_collisions(new_hails, True)
    if collision:
        print(round(sum(collision)))
        break
