import re
import numpy as np
from pprint import pp

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)

v = np.array([[c for c in line] for line in lines])

strs = []
for i in range(dim):
    strs.append("".join(v[i, :]))
    strs.append("".join(v[:, i]))

v_lr = np.fliplr(v)
for i in range(-dim + 1, dim):
    strs.append("".join(v.diagonal(i)))
    strs.append("".join(v_lr.diagonal(i)))

count = 0
for s in strs:
    m = re.findall("XMAS", s)
    count = count + len(m)
    s_rev = s[::-1]
    m = re.findall("XMAS", s_rev)
    count = count + len(m)
print(count)

count = 0
for i in range(dim):
    for j in range(dim):
        v_sub = v[i:i + 3, j:j + 3]
        v_sub_lr = np.fliplr(v_sub)
        d1 = "".join(v_sub.diagonal())
        d2 = "".join(v_sub_lr.diagonal())
        if (d1 == "MAS" or d1[::-1] == "MAS") and (d2 == "MAS" or d2[::-1] == "MAS"):
            count = count + 1
print(count)
