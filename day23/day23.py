from collections import defaultdict, deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def get_elves():
    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == "#":
                elves.add((x, y))
    return elves


def empty_spaces(elves):
    min_x, min_y = min({p[0] for p in elves}), min({p[1] for p in elves})
    max_x, max_y = max({p[0] for p in elves}), max({p[1] for p in elves})
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def surround8(p):
    deltas = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    return {(p[0] + d[0], p[1] + d[1]) for d in deltas}


def north3(p):
    deltas = [1, 0, -1]
    return {(p[0] + d, p[1] - 1) for d in deltas}


def south3(p):
    deltas = [1, 0, -1]
    return {(p[0] + d, p[1] + 1) for d in deltas}


def east3(p):
    deltas = [1, 0, -1]
    return {(p[0] + 1, p[1] + d) for d in deltas}


def west3(p):
    deltas = [1, 0, -1]
    return {(p[0] - 1, p[1] + d) for d in deltas}


def dir4(p):
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    return [(p[0] + d[0], p[1] + d[1]) for d in deltas]


def sim(max_rounds=None):
    elves = get_elves()
    count = 0
    while True:
        proposed = defaultdict(list)
        for e in elves:
            surrounds = surround8(e)
            if not surrounds & elves:
                continue
            proposed_dirs = deque([north3, south3, west3, east3])
            proposed_pts = deque(dir4(e))
            proposed_dirs.rotate(-count)
            proposed_pts.rotate(-count)

            for f, proposed_p in zip(proposed_dirs, proposed_pts):
                view = f(e)
                if not view & elves:
                    proposed[proposed_p].append(e)
                    break

        moved = False
        for proposed_p, proposers in proposed.items():
            if len(proposers) > 1:
                continue
            elves.remove(proposers[0])
            elves.add(proposed_p)
            moved = True

        count += 1
        if not moved or (max_rounds is not None and count >= max_rounds):
            break
    return count, empty_spaces(elves)


# part 1
_, empty_count = sim(10)
print(empty_count)

# part 2
count, _ = sim()
print(count)
