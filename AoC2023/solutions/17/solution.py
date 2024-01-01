# Advent of Code 2023 day 17
from util import *
from bisect import bisect

YEAR = 2023
DAY = 17


def get_data():
    arr = input_array(DAY, YEAR)
    return [[int(i) for i in line] for line in arr]


def is_oob(x, y):
    return not (0 <= x < len(data[0]) and 0 <= y < len(data))


directions = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1),
}

turns = {
    ">": "v^",
    "<": "v^",
    "v": "<>",
    "^": "<>",
}


def expand(x, y, direction, min_d, max_d):
    for d in turns[direction]:
        total = 0
        dx, dy = directions[d]
        for i in range(1, max_d + 1):
            nx, ny = x + dx * i, y + dy * i
            if is_oob(nx, ny):
                continue
            total += data[ny][nx]
            if i < min_d:
                continue
            if 0 <= nx < len(data[0]) and 0 <= ny < len(data):
                yield nx, ny, total, d


def to_end(x, y):
    return width - x - 1 + height - y - 1


def run(min_d, max_d):
    visited = set()
    to_visit = [(0, 0, 0, "<"), (0, 0, 0, "^")]

    while to_visit:
        x, y, dist, direction, _ = to_visit.pop(0)
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))
        if to_end(x, y) == 0:
            return dist
        for nx, ny, total, nd in expand(x, y, direction, min_d, max_d):
            total_dist = dist + total
            i = bisect(to_visit, total_dist, key=lambda l: l[2])
            to_visit.insert(i, (nx, ny, total_dist, nd))


data = get_data()
width, height = len(data[0]), len(data)

first = run(0, 3)
second = run(4, 10)

print("First:  ", first)
print("Second: ", second)
