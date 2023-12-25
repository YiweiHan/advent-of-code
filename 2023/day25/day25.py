from random import randint

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

edges = set()
vertices = set()
for line in lines:
    name, rem = line.split(": ")
    other_names = rem.split(" ")
    vertices.add(name)
    for o in other_names:
        vertices.add(o)
        edges.add((name, o))

edges = list(edges)


def contract():
    result_groups = [{v} for v in vertices]

    while len(result_groups) > 2:
        edge = edges[randint(0, len(edges) - 1)]
        g1_idx = g2_idx = None
        for i, g in enumerate(result_groups):
            if edge[0] in g:
                g1_idx = i
            elif edge[1] in g:
                g2_idx = i
            if g1_idx is not None and g2_idx is not None:
                break
        if g1_idx == g2_idx or g1_idx is None or g2_idx is None:
            continue
        result_groups[g1_idx].update(result_groups[g2_idx])
        result_groups.pop(g2_idx)
    return result_groups


def valid_cut(g1, g2):
    cuts = 0
    for v1, v2 in edges:
        if (v1 in g1 and v2 in g2) or (v2 in g1 and v1 in g2):
            if cuts == 3:
                return False
            cuts = cuts + 1
    return cuts == 3


while True:
    g1, g2 = contract()
    if valid_cut(g1, g2):
        print(len(g1) * len(g2))
        break
