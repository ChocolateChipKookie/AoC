# Advent of Code 2023 day 16
from util import *

YEAR = 2023
DAY = 16


def get_data():
    return input_array(DAY, YEAR)


moves = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

reflections = {
    "\\": {
        ">": "v",
        "<": "^",
        "v": ">",
        "^": "<",
    },
    "/": {
        ">": "^",
        "<": "v",
        "v": "<",
        "^": ">",
    },
}


def is_oob(x, y):
    return not (0 <= x < len(data[0]) and 0 <= y < len(data))


def run(x, y, direction):
    visited = set()
    to_visit = [(x, y, direction)]

    while to_visit:
        x, y, direction = to_visit.pop(0)
        if is_oob(x, y):
            continue

        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        current = data[y][x]
        dx, dy = moves[direction]
        if (
            current == "."
            or (direction in "<>" and current == "-")
            or (direction in "^v" and current == "|")
        ):
            to_visit.append((x + dx, y + dy, direction))
            continue

        if current == "|":
            to_visit.append((x, y + 1, "v"))
            to_visit.append((x, y - 1, "^"))
            continue

        if current == "-":
            to_visit.append((x + 1, y, ">"))
            to_visit.append((x - 1, y, "<"))
            continue

        direction = reflections[current][direction]
        dx, dy = moves[direction]
        to_visit.append((x + dx, y + dy, direction))

    return len(set((x, y) for x, y, _ in visited))


data = get_data()

first = run(0, 0, ">")

starts = [
    *((i, 0, "v") for i in range(len(data[0]))),
    *((i, len(data) - 1, "^") for i in range(len(data[0]))),
    *((0, i, ">") for i in range(len(data))),
    *((len(data[0]) - 1, i, "<") for i in range(len(data))),
]
second = max(run(*args) for args in starts)

print("First:  ", first)
print("Second: ", second)
