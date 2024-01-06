# Advent of Code 2023 day 9
from util import *

YEAR = 2023
DAY = 9


def get_data() -> list[list[int]]:
    return [[int(i) for i in l.split()] for l in input_lines(DAY, YEAR)]


def create_levels(history: list[int]) -> list[list[int]]:
    levels: list[list[int]] = [history]

    while any(x != 0 for x in levels[-1]):
        latest = levels[-1]
        levels.append([x2 - x1 for x1, x2 in zip(latest[:-1], latest[1:])])
    return levels


def extrapolate_next(history: list[int]) -> int:
    levels = create_levels(history)
    return sum(l[-1] for l in levels)


def extrapolate_previous(history: list[int]) -> int:
    levels = create_levels(history)
    current = 0
    for level in levels[::-1]:
        current = level[0] - current
    return current


data = get_data()

first = sum(extrapolate_next(d) for d in data)
second = sum(extrapolate_previous(d) for d in data)

print("First:  ", first)
print("Second: ", second)
