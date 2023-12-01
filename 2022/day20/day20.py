from collections import deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

input = list(map(int, lines))


def mix(decrypt_key=1, mix_rounds=1):
    msg = [n * decrypt_key for n in input]

    shifted_idxs = {i: i for i in range(len(msg))}

    shifted = deque(msg)

    for round in range(mix_rounds):
        for i in range(len(msg)):
            curr_num = msg[i]

            if curr_num == 0:
                continue

            curr_idx = shifted_idxs[i]

            shifted.rotate(-curr_idx - 1)
            for j in shifted_idxs.keys():
                shifted_idxs[j] = (shifted_idxs[j] - curr_idx - 1) % len(msg)

            shifted.pop()
            shifted.rotate(-curr_num)
            shifted.append(curr_num)
            shifted_idxs = {k: (v if v == (len(msg) - 1) else (v - curr_num) % (len(msg) - 1)) for k, v in shifted_idxs.items()}

    zero_idx = shifted.index(0)
    print(sum([shifted[(zero_idx + i * 1000) % len(shifted)] for i in range(1, 4)]))


mix()
mix(811589153, 10)
