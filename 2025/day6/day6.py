import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

lines2 = [re.split("\\s+", l.strip()) for l in lines]

nums = [[int(x) for x in l] for l in lines2[:-1]]
ops = lines2[-1]

c = 0
for i, o in enumerate(ops):
    ns = [nums[j][i] for j in range(len(nums))]
    st = o.join([str(n) for n in ns])
    c += eval(st)
print(c)


nums = lines[:-1]

op_i = len(ops) - 1
cols = max([len(nums[i]) for i in range(len(nums))])
nums_c = cols - 1
q = []
c = 0
while True:
    if nums_c < 0:
        st = ops[op_i].join(q)
        c += eval(st)
        break
    ns = [nums[r][nums_c] if len(nums[r]) > nums_c else '' for r in range(len(nums))]
    ns = "".join(ns).strip()
    if ns == "":
        st = ops[op_i].join(q)
        c += eval(st)
        op_i -= 1
        q.clear()
    else:
        q.append(ns)
    nums_c -= 1

print(c)
