import re


with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def combinations(seq, nums):
    cache = {}

    def recurse(seq, nums):
        if (seq, nums) in cache:
            return cache[(seq, nums)]

        if len(seq) == 0 or all(c == "." for c in seq):
            result = len(nums) == 0
        elif len(nums) == 0:
            result = all(c == "?" or c == "." for c in seq)
        elif seq[0] == ".":
            result = recurse(seq[1:], nums)
        elif seq[0] == "?":
            test_seq1 = (".",) + seq[1:]
            test_seq2 = ("#",) + seq[1:]
            result = recurse(test_seq1, nums) + recurse(test_seq2, nums)
        else:
            test_group, rest = seq[:nums[0]], seq[nums[0]:]
            if len(test_group) == nums[0] and all(c != "." for c in test_group):
                if len(rest) == 0:
                    result = recurse(rest, nums[1:])
                elif rest[0] == "#":
                    result = 0
                else:
                    result = recurse((".",) + rest[1:], nums[1:])
            else:
                result = 0
        cache[(seq, nums)] = result
        return result

    return recurse(seq, nums)


rows = []
for line in lines:
    seq, nums = re.split(r" ", line)
    seq = tuple([*seq])
    nums = tuple(int(x) for x in re.split(r",", nums))
    rows.append((seq, nums))


def total_combinations(multiplier):
    total = 0
    for seq, nums in rows:
        multiplied_seq = tuple([*"?".join(["".join(seq)] * multiplier)])
        multiplied_nums = nums * multiplier
        total = total + combinations(multiplied_seq, multiplied_nums)
    return total


# part 1
print(total_combinations(1))

# part 2
print(total_combinations(5))
