import re
from itertools import groupby, product
from functools import reduce

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

workflows_lines, ratings_lines = [list(i[1]) for i in groupby(lines, lambda i: i != '') if i[0]]

workflows = {}
for line in workflows_lines:
    name, rules, _ = re.split(r"[{}]", line)
    rules = re.split(r",", rules)
    rules = [tuple(re.split(r":", r)) if ":" in r else r for r in rules]
    workflows[name] = rules

ratings = [tuple(int(x) for x in re.split(r"[{},xmas=]+", line) if x != '') for line in ratings_lines]

starting_workflow = "in"

category_indexes = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3,
}


def sum_categories(ranges):
    return sum(sum(x) for x in product(*[range(r[0], r[1] + 1) for r in ranges]))


def count_ranges(ranges):
    return reduce(lambda x, y: x * y, [r[1] - r[0] + 1 for r in ranges])


def split_eval_ranges(ranges, condition):
    category_idx, compare, value = category_indexes[condition[0]], condition[1], int(condition[2:])
    v1, v2 = ranges[category_idx]
    if (compare == "<" and v2 < value) or (compare == ">" and v1 > value):
        return True
    if (compare == "<" and v1 >= value) or (compare == ">" and v2 <= value):
        return False
    new_category_ranges = []
    if compare == "<" and v1 < value <= v2:
        new_category_ranges = (v1, value - 1), (value, v2)
    if compare == ">" and v1 <= value < v2:
        new_category_ranges = (v1, value), (value + 1, v2)
    new_ranges = [ranges[:], ranges[:]]
    for i in range(2):
        new_ranges[i][category_idx] = new_category_ranges[i]
    return new_ranges


def eval_ranges(ranges, accept_func):
    wf_name = starting_workflow

    while True:
        for rule in workflows[wf_name]:
            if isinstance(rule, str):
                if rule == "A":
                    return accept_func(ranges)
                if rule == "R":
                    return 0
                else:
                    wf_name = rule
                    break

            condition, dest = rule
            result = split_eval_ranges(ranges, condition)
            if isinstance(result, bool):
                if result:
                    if dest == "A":
                        return accept_func(ranges)
                    if dest == "R":
                        return 0
                    else:
                        wf_name = dest
                        break
                else:
                    continue
            else:
                return result


def process(ranges, accept_func):
    total = 0
    q = [ranges]
    while len(q):
        cur_ranges = q.pop()
        result = eval_ranges(cur_ranges, accept_func)
        if isinstance(result, int):
            total = total + result
        else:
            q.extend(result)
    return total


# part 1
print(sum(process(ranges, sum_categories) for ranges in [[(x, x) for x in rating] for rating in ratings]))

# part 2
print(process([(1, 4000)] * 4, count_ranges))
