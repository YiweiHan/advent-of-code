import re
from collections import deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def build_initial():
    raw_nums = {}
    eqs = deque()
    root_eq = None
    for line in lines:
        if line.startswith("root"):
            root_eq = line
            continue
        vals = list(map(int, re.findall("[0-9]+", line)))
        if vals:
            raw_nums[line[:4]] = vals[0]
        else:
            eqs.append(line)
    return raw_nums, eqs, root_eq


nums, eqs, root_eq = build_initial()
eqs.append(root_eq)


def try_eval(nums, eq):
    op = eq[6:]
    a, b = re.split("[ */+-]+", op)
    if a in nums and b in nums:
        num_a, num_b = nums[a], nums[b]
        nums[eq[:4]] = eval("num_a" + op[5] + "num_b")
        return True
    return False


def solve(nums, eqs, try_function):
    while eqs:
        new_num = False
        for _ in range(len(eqs)):
            eq = eqs.popleft()
            if try_function(nums, eq):
                new_num = True
            else:
                eqs.append(eq)
        if not new_num:
            break


solve(nums, eqs, try_eval)

# part 1
print(int(nums["root"]))

nums, eqs, root_eq = build_initial()
nums.pop("humn")

solve(nums, eqs, try_eval)

root_var1, root_var2 = re.split("[ */+-]+", root_eq.replace("root: ", ""))
eq_num, find_var = (nums[root_var1], root_var2) if root_var1 in nums else (nums[root_var2], root_var1)
nums[find_var] = eq_num


def try_solve_args(nums, eq):
    labels = re.findall("[a-z]{4}", eq)
    o = eq[11]

    # x: a op b
    if labels[0] in nums and labels[2] in nums:
        inv_o = "*" if o == "/" else "+" if o == "-" else "/" if o == "*" else "-"
        num_x, num_b = nums[labels[0]], nums[labels[2]]
        nums[labels[1]] = eval("num_x" + inv_o + "num_b")
        return True
    if labels[0] in nums and labels[1] in nums:
        num_x, num_a = nums[labels[0]], nums[labels[1]]
        if o == "-" or o == "/":
            nums[labels[2]] = eval("num_a" + o + "num_x")
        else:
            inv_o = "/" if o == "*" else "-"
            nums[labels[2]] = eval("num_x" + inv_o + "num_a")
        return True
    return False


solve(nums, eqs, try_solve_args)

# part 2
print(int(nums["humn"]))
