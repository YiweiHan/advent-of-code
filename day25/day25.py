with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def to_dec(s):
    def map_int(c):
        return -2 if c == "=" else -1 if c == "-" else int(c)
    return sum([(5 ** i) * map_int(c) for i, c in enumerate(reversed(s))])


def to_snafu(n):
    def to_char(i):
        return "=" if i == -2 else "-" if i == -1 else str(i)
    carry = 0
    s = ""
    while n + carry > 0:
        n, rem = divmod(n + carry, 5)
        if rem > 2:
            carry = 1
            s += to_char(rem - 5)
        else:
            carry = 0
            s += to_char(rem)
    return s[::-1]


print(to_snafu(sum([to_dec(l) for l in lines])))
