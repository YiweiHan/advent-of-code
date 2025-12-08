with open("input.txt", "r") as f:
    lines = f.read().splitlines()

nums = [[int(y) for y in x] for x in lines]


def find_(seq, l):
    if not seq or l == 0:
        return []
    max_p_seq = max(seq[0:len(seq) - l + 1])
    res = []

    for i in range(0, len(seq) - l + 1):
        if seq[i] != max_p_seq:
            continue
        d = seq[i]
        r = seq[i+1:]
        nexts = find_(r, l - 1)
        if not nexts:
            res.append([d])
        else:
            for nx in nexts:
                res.append([d] + nx)
    return res

s1 = 0
s2 = 0
for n in nums:
    f1 = find_(n, 2)
    f2 = find_(n, 12)
    s1 += max([int("".join([str(y) for y in x])) for x in f1])
    s2 += max([int("".join([str(y) for y in x])) for x in f2])
print(s1)
print(s2)
