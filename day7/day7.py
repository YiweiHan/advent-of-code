import re
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

dir_tree = defaultdict(list)

file_sizes = {}

wd = "/"
for line in lines[1:]:
    if line.startswith("$ ls"):
        continue
    if line.startswith("$ cd"):
        new_dir = re.split(" ", line)[2]
        if new_dir == "..":
            wd = wd[0:wd[:wd.rfind("/")].rfind("/")] + "/"
        else:
            wd += new_dir + "/"
    else:
        s1, s2 = re.split(" ", line)
        if s1 == "dir":
            dir_tree[wd].append(wd + s2 + "/")
        else:
            file_sizes[wd + s2] = int(s1)


dir_total_sizes = {}


def size_dir(parent_dir):
    total_size_files = 0
    for file, size in file_sizes.items():
        if file.startswith(parent_dir) and "/" not in file[len(parent_dir):]:
            total_size_files += size

    total_size_children = 0
    for child_dir in dir_tree[parent_dir]:
        total_size_children += size_dir(child_dir)
    total_size = total_size_files + total_size_children
    dir_total_sizes[parent_dir] = total_size
    return total_size


used_space = size_dir("/")

total_max_100k = 0
for d, size in dir_total_sizes.items():
    if size <= 100000:
        total_max_100k += size

print(total_max_100k)


total_disk = 70000000
update_required_space = 30000000
free_space = total_disk - used_space
space_to_delete = update_required_space - free_space

min_num = total_disk
delete_dir = None
for d, size in dir_total_sizes.items():
    if space_to_delete <= size < min_num:
        min_num = size
        delete_dir = d

print(dir_total_sizes[delete_dir])
