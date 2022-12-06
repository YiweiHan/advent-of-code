with open("input.txt", "r") as f:
    lines = f.read().splitlines()

line = lines[0]


def marker(window_len):
    for i in range(window_len, len(line)):
        window = line[i - window_len:i]
        if len(set(window)) == len(window):
            return i


print(marker(4))
print(marker(14))
