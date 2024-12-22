import re
from itertools import product

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

ls = []
for line in lines:
    n, ns = re.split(": ", line)
    ls.append((int(n), tuple(int(x) for x in re.split(" ", ns))))

print(ls)

ops1 = ['+', '*']
ops2 = ['+', '*', '|']


def eval_eq(ns, ops_arrange):
    cur = ns[0]
    for op, n in zip(ops_arrange, ns[1:]):
        if op == '+':
            cur = cur + n
        elif op == '*':
            cur = cur * n
        else:
            cur = int(str(cur) + str(n))
    return cur


def calib(ops):
    s = 0
    for res, ns in ls:
        ops_arranges = list(product(ops, repeat=len(ns) - 1))
        for ops_arrange in ops_arranges:
            cur_res = eval_eq(ns, ops_arrange)
            if cur_res == res:
                s = s + res
                break
    return s


print(calib(ops1))
print(calib(ops2))
