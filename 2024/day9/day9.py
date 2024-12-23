from collections import defaultdict
from copy import deepcopy

with open("input.txt", "r") as f:
    line = f.read().splitlines()[0]

blocks = defaultdict(list)
free = []
free_blocks = []

is_block = True
next_block_id = 0
cur_idx = 0
for i, c in enumerate(line):
    n = int(c)
    segment = list(range(cur_idx, cur_idx + n))
    if is_block:
        blocks[next_block_id].extend(segment)
        next_block_id = next_block_id + 1
    elif n > 0:
        free.extend(segment)
        free_blocks.append((cur_idx, cur_idx + n))
    cur_idx = cur_idx + n
    is_block = not is_block


def find_last_block_idx(blocks):
    last_block_id = None
    last_block_idx = None
    for block_id, block_idxs in blocks.items():
        for idx in block_idxs:
            if last_block_idx is None or idx > last_block_idx:
                last_block_id = block_id
                last_block_idx = idx
    return last_block_id, last_block_idx


def defrag_blocks(blocks):
    for f_idx in free:
        last_id, last_block_idx = find_last_block_idx(blocks)
        if last_block_idx < f_idx:
            break
        blocks[last_id].remove(last_block_idx)
        blocks[last_id].insert(0, f_idx)
    return blocks


def checksum(blocks):
    s = 0
    for block_id, block_idxs in blocks.items():
        for idx in block_idxs:
            s = s + block_id * idx
    return s


print(checksum(defrag_blocks(deepcopy(blocks))))


def shift_blocks(blocks, free_blocks):
    def insert(new_free):
        for i, f_seg in reversed(list(enumerate(free_blocks))):
            if f_seg[1] <= new_free[0]:
                free_blocks.insert(i + 1, new_free)
                break
            if i == 0:
                free_blocks.insert(0, new_free)
        while True:
            merged = False
            for i, f_seg_r in reversed(list(enumerate(free_blocks))):
                if i == 0:
                    break
                f_seg_l = free_blocks[i - 1]
                if f_seg_l[1] >= f_seg_r[0]:
                    merged_free = f_seg_l[0], f_seg_r[1]
                    free_blocks[i - 1] = merged_free
                    free_blocks.pop(i)
                    merged = True

            if not merged:
                break

    prev_block_id = len(blocks.keys()) + 1
    while prev_block_id > 0:
        valid_ids = filter(lambda x: x < prev_block_id, list(blocks.keys()))
        next_block_id = sorted(valid_ids)[-1]
        block_idxs = blocks[next_block_id]
        for f_idx, f_seg in enumerate(free_blocks):
            if len(block_idxs) <= (f_seg[1] - f_seg[0]) and f_seg[0] < block_idxs[0]:
                blocks[next_block_id] = list(range(f_seg[0], f_seg[0] + len(block_idxs)))
                remain = (f_seg[0] + len(block_idxs), f_seg[1])
                free_blocks.remove(f_seg)
                if remain[1] - remain[0] != 0:
                    free_blocks.insert(f_idx, remain)
                new_free = (block_idxs[0], block_idxs[0] + len(block_idxs))
                insert(new_free)
                break
        prev_block_id = next_block_id

    return blocks


print(checksum(shift_blocks(deepcopy(blocks), deepcopy(free_blocks))))
