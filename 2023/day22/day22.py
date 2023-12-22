import re
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

bricks = set()
for line in lines:
    nums = [int(x) for x in re.split(r"[,~]", line)]
    bricks.add(((nums[0], nums[3]), (nums[1], nums[4]), (nums[2], nums[5])))

bricks = sorted(bricks, key=lambda b: b[2][0])


def settle(bricks):
    height = defaultdict(lambda: defaultdict(int))
    settled = []
    fell = 0
    for x_r, y_r, z_r in bricks:
        cur_max_height = max(height[x][y] for x in range(x_r[0], x_r[1] + 1) for y in range(y_r[0], y_r[1] + 1))
        new_z_r = cur_max_height + 1, z_r[1] - z_r[0] + cur_max_height + 1
        if new_z_r != z_r:
            fell = fell + 1
        settled.append((x_r, y_r, new_z_r))
        cur_new_height = cur_max_height + z_r[1] - z_r[0] + 1
        for x in range(x_r[0], x_r[1] + 1):
            for y in range(y_r[0], y_r[1] + 1):
                height[x][y] = cur_new_height
    return settled, fell


settled, _ = settle(bricks)
total_can_disintegrate = 0
total_fell = 0
for candidate in settled:
    remaining = [b for b in settled if b != candidate]
    _, fell = settle(remaining)
    total_fell = total_fell + fell
    if not fell:
        total_can_disintegrate = total_can_disintegrate + 1

# part 1
print(total_can_disintegrate)

# part 2
print(total_fell)
