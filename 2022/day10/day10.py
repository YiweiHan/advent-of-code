import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

cmds = list(map(lambda l: (2, int(re.split(" ", l)[1])) if l[0] == "a" else (1, 0), lines))
total_cycles = sum(map(lambda cmd: cmd[0], cmds))

x_reg = 1
curr_cmd = None
sum_signal = 0
buf = []

for c in range(total_cycles):
    if len(cmds) > 0 and curr_cmd is None:
        curr_cmd = cmds.pop(0)

    buf.append("#" if abs(c % 40 - x_reg) <= 1 else ".")

    if (c - 19) % 40 == 0:
        sum_signal += (c + 1) * x_reg

    if curr_cmd is not None:
        curr_cmd = (curr_cmd[0] - 1, curr_cmd[1])
        if curr_cmd[0] == 0:
            x_reg += curr_cmd[1]
            curr_cmd = None

print(sum_signal)

for y in range(6):
    print("".join(buf[y * 40:(y + 1) * 40]))
