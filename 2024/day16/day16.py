from collections import deque, defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)


def value(p):
    return lines[p[0]][p[1]]


def next_pos(p, d):
    vec = {
        0: (-1, 0),
        1: (0, 1),
        2: (1, 0),
        3: (0, -1),
    }[d]
    return p[0] + vec[0], p[1] + vec[1]


def is_junction(coord):
    ns = [next_pos(coord, i) for i in range(4)]
    v = "".join([value(n) for n in ns])
    v = v.replace("E", ".")
    v = v.replace("S", ".")
    if v.count('.') > 2 or v.count('.') == 1:
        return True
    return v == "##.." or v == ".##." or v == "..##" or v == "#..#"


start = end = None
d = 1
junctions = set()
for r in range(dim):
    for c in range(dim):
        v = value((r, c))
        if v == 'S':
            start = (r, c)
        if v == 'E':
            end = (r, c)
        if v == 'S' or v == 'E' or (v == '.' and is_junction((r, c))):
            junctions.add((r, c))


def next_junction(p, d):
    pn = p
    i = 0
    while True:
        pn = next_pos(pn, d)
        if value(pn) == '#':
            break
        i += 1
        if pn in junctions:
            return pn, i
    return None


def next_state_turn(cur, d, score, turn):
    di = d
    for i in range(1, 3):
        di = (di + turn) % 4
        n = next_pos(cur, di)
        if value(n) != '#':
            return cur, di, score + i * 1000
    return None


def next_states(cur, d, score, prev):
    states = []
    n = next_junction(cur, d)
    if n is not None:
        nx, delta = n
        states.append((nx, d, score + delta))
    next_r = next_state_turn(cur, d, score, 1)
    next_l = next_state_turn(cur, d, score, -1)
    if next_l is not None and next_r is not None and next_l[0:2] == next_r[0:2] and next_l[0:2] != prev:
        states.append((next_l[0], next_l[1], min(next_l[2], next_r[2])))
    else:
        if next_l is not None and next_l != prev:
            states.append(next_l)
        if next_r is not None and next_r != prev:
            states.append(next_r)
    return [state for state in states if state[0:2] != (cur, d)]


def search(start_state):
    q = deque([start_state])
    min_scores_at = defaultdict(int)
    min_score = None
    paths = []
    while q:
        cur, d, score, path = q.popleft()
        if (cur, d) in min_scores_at:
            if score > min_scores_at[(cur, d)]:
                continue
            elif score < min_scores_at[(cur, d)]:
                min_scores_at[(cur, d)] = score
        else:
            min_scores_at[(cur, d)] = score
        if cur == end:
            if min_score is None or score < min_score:
                min_score = score
                paths.clear()
                paths.append(path)
            elif min_score is not None and score == min_score:
                paths.append(path)
            continue
        prev = path[-2] if len(path) > 1 else None
        nexts = next_states(cur, d, score, prev)
        nexts = [(p, di, sc, path + [(p, di)]) for p, di, sc in nexts if
                 (p, di) not in path and p not in set(x for x, _ in path[:-1])]
        q.extend(nexts)

    return min_score, paths


def gen_pts(f, t):
    if f == t:
        return
    diff = t[0] - f[0], t[1] - f[1]
    if diff[0] != 0:
        vec = (diff[0] // abs(diff[0]), 0)
    else:
        vec = (0, diff[1] // abs(diff[1]))

    c = abs(diff[0]) + abs(diff[1])
    p = f
    for i in range(c - 1):
        p = (p[0] + vec[0], p[1] + vec[1])
        yield p


state = (start, d, 0, [(start, d)])

min_score, paths = search(state)
print(min_score)

pts = set()
for path in paths:
    for i in range(1, len(path)):
        pts.update([path[i - 1][0], path[i][0]])
        pts.update(gen_pts(path[i - 1][0], path[i][0]))

print(len(pts))
