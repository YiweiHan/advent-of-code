import re
from itertools import product

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def overlap_obj(obj1, obj2):
    if obj1 == obj2:
        return obj1

    x1, x1_end, y1, y1_end, z1, z1_end = obj1
    x2, x2_end, y2, y2_end, z2, z2_end = obj2

    if x1_end < x2 or x2_end < x1 or y1_end < y2 or y2_end < y1 or z1_end < z2 or z2_end < z1:
        return None

    return max(x1, x2), min(x1_end, x2_end), max(y1, y2), min(y1_end, y2_end), max(z1, z2), min(z1_end, z2_end)


def split(obj, ov_obj):
    def segments(s, s_end, ovs, ovs_end):
        return list(filter(lambda v: s <= v[0] <= s_end and s <= v[1] <= s_end, [(s, ovs - 1), (ovs, ovs_end), (ovs_end + 1, s_end)]))

    if obj == ov_obj:
        return []
    x, x_end, y, y_end, z, z_end = obj
    ovx, ovx_end, ovy, ovy_end, ovz, ovz_end = ov_obj

    x_segments = segments(x, x_end, ovx, ovx_end)
    y_segments = segments(y, y_end, ovy, ovy_end)
    z_segments = segments(z, z_end, ovz, ovz_end)

    return list(filter(lambda o: o != ov_obj, [(vx, vx_end, vy, vy_end, vz, vz_end) for (vx, vx_end), (vy, vy_end), (vz, vz_end) in product(x_segments, y_segments, z_segments)]))


steps = list(map(lambda step: (step[1] == "n",) + tuple(map(int, list(filter(None, re.split("[a-z =,.]+", step))))), lines))


def count(steps):
    objs = []
    for step in steps:
        new_obj = step[1:]
        if len(objs) == 0 and step[0]:
            objs.append(new_obj)
        else:
            split_objs = []
            for o in objs:
                ov_obj = overlap_obj(o, new_obj)
                if ov_obj is None:
                    split_objs.append(o)
                    continue
                split_objs.extend(split(o, ov_obj))
            if step[0]:
                split_objs.append(new_obj)
            objs = split_objs
    return sum(map(lambda obj: (obj[1] - obj[0] + 1) * (obj[3] - obj[2] + 1) * (obj[5] - obj[4] + 1), objs))


print(count(steps[0:20]))
print(count(steps))
