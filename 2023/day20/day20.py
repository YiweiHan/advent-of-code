from collections import deque, defaultdict
from math import lcm

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

modules = {}
flipflops_state = {}
conjunctions = set()

for line in lines:
    module, dests = line.split(" -> ")
    if module[0] == "%":
        module = module[1:]
        flipflops_state[module] = False
    elif module[0] == "&":
        module = module[1:]
        conjunctions.add(module)
    modules[module] = dests.split(", ")

conjunction_inputs = defaultdict(dict)
for module, dests in modules.items():
    for conjunction in conjunctions:
        if conjunction in dests:
            conjunction_inputs[conjunction][module] = False


def push_button(watch=None):
    q = deque()
    q.append(("button", False, "broadcaster"))
    sent = [0, 0]
    high_emitted = [None] * len(watch) if watch else None

    while len(q):
        source, pulse, module = q.popleft()

        if watch is not None:
            for i, w in enumerate(watch):
                if w == source and pulse:
                    high_emitted[i] = True

        sent[pulse] = sent[pulse] + 1

        if module not in modules:
            continue

        dests = modules[module]
        if module in flipflops_state:
            if not pulse:
                flipflops_state[module] = not flipflops_state[module]
                for dest in dests:
                    q.append((module, flipflops_state[module], dest))
        elif module in conjunctions:
            conjunction_inputs[module][source] = pulse
            next_pulse = not all(conjunction_inputs[module].values())
            for dest in dests:
                q.append((module, next_pulse, dest))
        else:
            for dest in dests:
                q.append((module, pulse, dest))
    return sent, high_emitted


# part 1
all_sent = [push_button()[0] for _ in range(1000)]
print(sum(sent[0] for sent in all_sent) * sum(sent[1] for sent in all_sent))

# part 2
for m in flipflops_state.keys():
    flipflops_state[m] = False
for m, inputs in conjunction_inputs.items():
    for k in inputs.keys():
        inputs[k] = False

target = "rx"
conjunction1 = [source for source, dests in modules.items() if target in dests][0]
watch = list(conjunction_inputs[conjunction1].keys())
pushes = 0
cycles = [None] * len(watch)
while True:
    _, high_emitted = push_button(watch)
    pushes = pushes + 1
    for i, e in enumerate(high_emitted):
        if cycles[i] is None and e is not None:
            cycles[i] = pushes
    if all(c is not None for c in cycles):
        break
print(lcm(*cycles))
