with open("input.txt", "r") as f:
    lines = f.read().splitlines()

r = 12
g = 13
b = 14


def eval_round(rounds):
    possible = True
    max_r = max_g = max_b = 0
    for round in rounds:
        items = round.split(", ")
        for item in items:
            n, colour = item.split(" ")
            n = int(n)
            if (colour == "red" and n > r) or (colour == "green" and n > g) or (colour == "blue" and n > b):
                possible = False
            if colour == "red" and n > max_r:
                max_r = n
            if colour == "green" and n > max_g:
                max_g = n
            if colour == "blue" and n > max_b:
                max_b = n
    return possible, max_r * max_g * max_b


total_id = 0
total_power = 0

for line in lines:
    parts = line.split(": ")
    game_id = int(parts[0].split(" ")[1])
    rounds = parts[1].split("; ")
    possible, power = eval_round(rounds)
    if possible:
        total_id = total_id + game_id
    total_power = total_power + power

# part 1
print(total_id)
# part 2
print(total_power)
