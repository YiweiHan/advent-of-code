with open("input.txt", "r") as f:
    lines = f.read().splitlines()

line = lines[0]


def marker(window_len):
    for i in range(window_len, len(line)):
        if len(set(line[i - window_len:i])) == window_len:
            return i


print(marker(4))
print(marker(14))
