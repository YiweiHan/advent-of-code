import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def calc(lines, ignore_flags):
    s = 0
    enabled = True
    for line in lines:
        matches = re.findall("do\\(\\)|don't\\(\\)|mul\\([0-9]+,[0-9]+\\)", line)

        for m in matches:
            if m == "do()":
                enabled = True
            elif m == "don't()":
                enabled = True if ignore_flags else False
            elif enabled:
                nums = re.findall("mul\\(([0-9]+),([0-9]+)\\)", m)[0]
                s = s + int(nums[0]) * int(nums[1])
    return s


print(calc(lines, True))
print(calc(lines, False))
