# Advent of Code 2023 day 15
from util import *

YEAR = 2023
DAY = 15


def get_data():
    return input_lines(DAY, YEAR)[0].split(",")


def calc_hash(line):
    total = 0
    for c in line:
        total += ord(c)
        total *= 17
        total %= 256
    return total


def get_commands():
    commands = []
    for cmd in get_data():
        if "-" in cmd:
            commands.append((cmd[:-1], "-", None))
        else:
            commands.append((cmd[:-2], "=", int(cmd[-1])))
    return commands


data = get_data()


hashmap = [[] for _ in range(256)]

first = sum(calc_hash(l) for l in data)

for label, action, count in get_commands():
    h = calc_hash(label)
    bucket = hashmap[h]
    index = next((i for i, (l, _) in enumerate(bucket) if l == label), None)
    if index is not None:
        if action == "-":
            bucket.pop(index)
        else:
            bucket[index][1] = count
    else:
        if action == "=":
            bucket.append([label, count])


second = 0
for i, lenses in enumerate(hashmap, 1):
    for j, (_, l) in enumerate(lenses, 1):
        second += i * j * l


print("First:  ", first)
print("Second: ", second)
