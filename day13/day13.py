from itertools import groupby
from functools import cmp_to_key

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

groups = [list(group) for k, group in groupby(lines, bool) if k]


def compare_lists(l1, l2):
    for item1, item2 in zip(l1, l2):
        if type(item1) == type(item2):
            if type(item1) == int:
                if item1 < item2:
                    return True
                if item1 > item2:
                    return False
            else:
                in_order = compare_lists(item1, item2)
                if in_order is not None:
                    return in_order
        else:
            in_order = compare_lists(item1 if type(item1) == list else [item1], item2 if type(item2) == list else [item2])
            if in_order is not None:
                return in_order
    return True if len(l1) < len(l2) else False if len(l1) > len(l2) else None


right_order_index_sum = 0
for index, (p1, p2) in enumerate(groups):
    pl1, pl2 = eval(p1), eval(p2)
    if compare_lists(pl1, pl2):
        right_order_index_sum += index + 1

print(right_order_index_sum)

all_packets = list(map(eval, filter(bool, ["[[2]]", "[[6]]"] + lines)))
sorted_packets = sorted(all_packets, key=cmp_to_key(lambda x, y: -1 if compare_lists(x, y) else 1))
divider_product = 1
for index, p in enumerate(sorted_packets):
    if p == [[2]] or p == [[6]]:
        divider_product *= (index + 1)
print(divider_product)
