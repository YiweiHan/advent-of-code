import re
from itertools import groupby
from collections import defaultdict
import math

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

monkey_props = [list(group) for k, group in groupby(lines, bool) if k]


def parse_monkey_props():
    monkeys = {}
    div_tests = []
    for p in monkey_props:
        m_id = int(re.split("[: ]", p[0])[1])
        start = list(map(int, re.split("[ :,]+", p[1])[3:]))
        op = "".join(re.split("[: =]+", p[2])[3:])
        div_test = int(re.split("[: ]+", p[3])[-1])
        div_tests.append(div_test)
        true_target = int(re.split("[: ]+", p[4])[-1])
        false_target = int(re.split("[: ]+", p[5])[-1])
        monkeys[m_id] = (start, op, div_test, true_target, false_target)

    # The product of all division tests.
    # Division testing against multiple numbers is cyclic over the product of all the test numbers.
    # To keep worry level low, they always have modulo mod_factor applied.
    mod_factor = math.prod(div_tests)
    return monkeys, mod_factor


def run_round(monkeys, inspections, mod_factor, div):
    def exec_op(old, op):
        v = eval(op) // div
        if div == 3:
            return v
        return v % mod_factor

    for m_id in monkeys.keys():
        items, op, div_test, true_target, false_target = monkeys[m_id]
        item_count = len(items)
        inspections[m_id] += item_count

        for _ in range(item_count):
            new = exec_op(items.pop(0), op)
            monkeys[true_target if new % div_test == 0 else false_target][0].append(new)


def run(rounds, div):
    inspections = defaultdict(int)
    monkeys, mod_factor = parse_monkey_props()
    for _ in range(rounds):
        run_round(monkeys, inspections, mod_factor, div)
    print(math.prod(list(reversed(sorted(inspections.values())))[0:2]))


run(20, 3)
run(10000, 1)
