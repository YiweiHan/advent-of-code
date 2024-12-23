from collections import defaultdict, deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dim = len(lines)


def nexts(cur):
    r, c = cur
    next_pos = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
    return set(filter(lambda p: 0 <= p[0] < dim and 0 <= p[1] < dim, next_pos))


coords_by_plot = defaultdict(set)
for r in range(dim):
    for c in range(dim):
        coords_by_plot[lines[r][c]].add((r, c))


def eval_plot(plot, coords):
    unused_coords = coords.copy()
    visited = set()
    regions = []

    def find_region():
        q = deque()
        q.append(list(unused_coords)[0])

        cur_region = set()
        cur_region_fences = 0
        while len(q):
            cur = q.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            unused_coords.remove(cur)
            cur_region.add(cur)
            neighbours = nexts(cur)
            joined = neighbours.intersection(coords)
            cur_region_fences = cur_region_fences + (4 - len(joined))
            q.extend(joined)
        return cur_region, cur_region_fences

    region_costs = 0
    while len(unused_coords):
        new_r, new_r_fences = find_region()
        regions.append(new_r)
        region_costs = region_costs + len(new_r) * new_r_fences

    return regions, region_costs


all_regions = []
s = 0
for p, coords in coords_by_plot.items():
    regions, plot_s = eval_plot(p, coords)
    s = s + plot_s
    all_regions.extend(regions)

print(s)


def sides(region):
    sides = 0
    for r, c in region:
        n = r - 1, c
        e = r, c + 1
        s = r + 1, c
        w = r, c - 1
        nw = r - 1, c - 1
        sw = r + 1, c - 1
        ne = r - 1, c + 1

        if n not in region and (w not in region or nw in region):
            sides = sides + 1

        if s not in region and (w not in region or sw in region):
            sides = sides + 1

        if w not in region and (n not in region or nw in region):
            sides = sides + 1

        if e not in region and (n not in region or ne in region):
            sides = sides + 1
    return sides


s = 0
for region in all_regions:
    s = s + sides(region) * len(region)
print(s)
