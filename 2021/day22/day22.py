import re
import numpy as np
from itertools import pairwise
import concurrent.futures


def step_in_bounds(s, dim, dim_end, idx):
    return s[idx[0]] <= dim <= s[idx[1]] or s[idx[0]] <= dim_end <= s[idx[1]]


def filter_steps(steps, dim, dim_end, idx):
    return [s for s in steps if step_in_bounds(s, dim, dim_end, idx)]


def proc_x(args):
    all_y, all_z, rev_steps, x, x_end = args
    count = 0
    filtered_steps_x = filter_steps(rev_steps, x, x_end-1, (1, 2))
    for y, y_end in pairwise(all_y):
        filtered_steps_y = filter_steps(filtered_steps_x, y, y_end-1, (3, 4))
        for z, z_end in pairwise(all_z):
            filtered_steps_z = filter_steps(filtered_steps_y, z, z_end-1, (5, 6))
            if filtered_steps_z and filtered_steps_z[0][0]:
                count += (x_end - x) * (y_end - y) * (z_end - z)
    return count


def parse_step(step):
    return (step[1] == "n",) + tuple(map(int, list(filter(None, re.split("[a-z =,.]+", step)))))


def to_item(v):
    return v.item()


def count_on(lines):
    steps = list(map(parse_step, lines))

    all_coords = np.zeros(shape=(len(steps), 6), dtype=np.int32)
    for i, step in enumerate(steps):
        all_coords[i, :] = list(step[1:])

    # normalize end coords
    all_x = list(map(to_item, sorted(set(list(all_coords[:, 0]) + list(all_coords[:, 1] + 1)))))
    all_y = list(map(to_item, sorted(set(list(all_coords[:, 2]) + list(all_coords[:, 3] + 1)))))
    all_z = list(map(to_item, sorted(set(list(all_coords[:, 4]) + list(all_coords[:, 5] + 1)))))

    rev_steps = list(reversed(steps))

    args = [(all_y, all_z, rev_steps, x_pair[0], x_pair[1]) for x_pair in pairwise(all_x)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        return sum(executor.map(proc_x, args, chunksize=10))


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.read().splitlines()
    print(count_on(lines[0:20]))
    print(count_on(lines))
