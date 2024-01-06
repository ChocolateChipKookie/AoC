# Advent of Code 2023 day 11
from util import *

YEAR = 2023
DAY = 11


def get_data():
    return input_array(DAY, YEAR)


def get_empty(data):
    return [i for i, line in enumerate(data) if all(c == "." for c in line)]


def calc_distance(s1, s2, factor):
    def calc(p1, p2, empty):
        l, r = min(p1, p2), max(p1, p2)
        empty_spaces = sum(1 for e in empty if e in range(l, r))
        return r - l + empty_spaces * (factor - 1)

    x_range, y_range = zip(s1, s2)
    dx = calc(*x_range, empty_columns)
    dy = calc(*y_range, empty_rows)
    return dx + dy


def calc_total(factor):
    def gen():
        for i, s1 in enumerate(stars[:-1]):
            for s2 in stars[i + 1 :]:
                yield calc_distance(s1, s2, factor)

    return sum(gen())


data = get_data()

empty_rows, empty_columns = get_empty(data), get_empty(zip(*data))
stars = list(get_positions_in_array(data, "#").keys())

first = calc_total(2)
second = calc_total(1_000_000)

print("First:  ", first)
print("Second: ", second)
