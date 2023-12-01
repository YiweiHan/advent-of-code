from itertools import islice

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def batched(iterable, batch_size):
    it = iter(iterable)
    while batch := list(islice(it, batch_size)):
        yield batch


def priority(item):
    return ord(item) + (27 - ord("A") if item < "a" else 1 - ord("a"))


# part 1
def line_priority_part1(line):
    (common_item,) = set.intersection(*map(set, batched(line, len(line)//2)))
    return priority(common_item)


print(sum(map(line_priority_part1, lines)))


# part 2
def line_triplet_priority_part2(line_triplet):
    (common_item,) = set.intersection(*map(set, line_triplet))
    return priority(common_item)


print(sum(map(line_triplet_priority_part2, batched(lines, 3))))
