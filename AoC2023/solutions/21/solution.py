# Advent of Code 2023 day 21
from util import *

YEAR = 2023
DAY = 21


def get_data():
    return input_array(DAY, YEAR)


def in_range(x, y):
    return 0 <= x < width and 0 <= y < height


neighbours = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def do_steps(steps, bounded=True):
    current_pos = set()
    next_pos = set()
    rocks = set()

    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "S":
                current_pos.add((x, y))
            if c == "#":
                rocks.add((x, y))

    for i in range(steps):
        for x, y in current_pos:
            for dx, dy in neighbours:
                pos = x + dx, y + dy
                if bounded and not in_range(*pos):
                    continue
                if (pos[0] % width, pos[1] % height) in rocks:
                    continue
                next_pos.add(pos)
        current_pos, next_pos = next_pos, current_pos
        next_pos.clear()

    return current_pos


def first():
    return len(do_steps(64))


def second():
    total_steps = 26501365
    total_radius = (total_steps - (width // 2)) // width
    mapping_steps = width // 2 + width * 2
    extended = do_steps(mapping_steps, False)
    quadrants = {}
    for x, y in extended:
        q = x // width, y // height
        quadrants[q] = quadrants.get(q, 0) + 1

    total = quadrants[0, 0]
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        total += quadrants[direction[0], direction[1]] * (total_radius - 1)
        total += quadrants[direction[0], direction[1] * 2] * total_radius

    for i in range(1, total_radius):
        if i % 2:
            total += i * quadrants[0, 1] * 4
        else:
            total += i * quadrants[0, 0] * 4

    for x, y in neighbours:
        total += quadrants[2 * x, 2 * y]

    return total


data = get_data()
width = len(data[0])
height = len(data)

print("First:  ", first())
print("Second: ", second())
