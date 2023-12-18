import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
dir_map = {
    "U": up,
    "D": down,
    "L": left,
    "R": right,
    "0": right,
    "1": down,
    "2": left,
    "3": up,
}

instructions = []
instructions2 = []
for line in lines:
    dir, num, hexa, _ = re.split(r"[ ()#]+", line)
    instructions.append((dir_map[dir], int(num)))
    instructions2.append((dir_map[hexa[5]], int(hexa[0:5], 16)))


def inside_polygon_area(vertices):
    sum1 = 0
    sum2 = 0
    for i in range(-1, len(vertices) - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]
    return abs(sum1 - sum2) / 2


def area(instructions):
    cur = (0, 0)
    vertices = []
    point_count = 0
    for dir, num in instructions:
        cur = cur[0] + dir[0] * num, cur[1] + dir[1] * num
        vertices.append(cur)
        point_count = point_count + num
    return int(inside_polygon_area(vertices)) + point_count // 2 + 1


# part 1
print(area(instructions))

# part 2
print(area(instructions2))
