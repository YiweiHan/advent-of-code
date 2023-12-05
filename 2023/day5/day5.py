import re
from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

sections = [list(i[1]) for i in groupby(lines, lambda i: i != '') if i[0]]

seeds_line = sections.pop(0)[0]
seed_vals = [int(x) for x in re.split(r"\s+", re.split(r":\s+", seeds_line)[1])]


section_maps = []
for s in sections:
    s.pop(0)
    m = []
    for row in s:
        nums = tuple(int(x) for x in re.split(r"\s+", row))
        m.append(nums)
    section_maps.append(m)


def min_location(seeds):
    min_loc = None
    for seed in seeds:
        cur_val = seed
        for maps in section_maps:
            for m in maps:
                if m[1] <= cur_val < (m[1] + m[2]):
                    cur_val = cur_val - m[1] + m[0]
                    break
        if min_loc is None or cur_val < min_loc:
            min_loc = cur_val
    return min_loc


# part 1
print(min_location(seed_vals))


def split_range(input_first, input_last, test_first, test_last):
    if input_last < test_first or input_first > test_last:
        # no overlap
        return None
    if input_first >= test_first and input_last <= test_last:
        # all input falls within test range
        return (input_first, input_last), None
    # partial overlap
    if input_first < test_first:
        return None, [(input_first, test_first - 1), (test_first, input_last)]
    return None, [(input_first, test_last), (test_last + 1, input_last)]


def map_ranges(input_ranges, section_mappings):
    mapped_ranges = []
    try_ranges = input_ranges[:]
    while len(try_ranges) > 0:
        cur_range = try_ranges.pop()
        processed = False
        for mapping in section_mappings:
            result = split_range(cur_range[0], cur_range[1], mapping[1], mapping[1] + mapping[2] - 1)
            if result is not None:
                pass_range, retry_ranges = result
                if retry_ranges:
                    try_ranges.extend(retry_ranges)
                    processed = True
                    break
                if pass_range:
                    new_range = (cur_range[0] - mapping[1] + mapping[0], cur_range[1] - mapping[1] + mapping[0])
                    mapped_ranges.append(new_range)
                    processed = True
                    break
        if not processed:
            mapped_ranges.append(cur_range)
    return mapped_ranges


# part 2
ranges = []
for i in range(0, len(seed_vals), 2):
    seed_start, seed_len = seed_vals[i], seed_vals[i + 1]
    ranges.append((seed_start, seed_start + seed_len - 1))

for section_map in section_maps:
    ranges = map_ranges(ranges, section_map)

print(min([min(x) for x in ranges]))
