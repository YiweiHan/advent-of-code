with open("input.txt", "r") as f:
    lines = f.read().splitlines()

line = lines[0]


def marker(window_len):
    window = []
    index = 1
    for c in line:
        window.append(c)
        if len(window) > window_len:
            window.pop(0)
        if len(set(window)) == len(window) == window_len:
            return index
        index += 1


print(marker(4))
print(marker(14))
