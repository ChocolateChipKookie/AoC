# Advent of Code 2023 day 6
from util import *
import math
from bisect import bisect

YEAR = 2023
DAY = 6


def get_data() -> list[list[int]]:
    lines = input_lines(DAY, YEAR)
    tokens = [line.split() for line in lines]
    inputs = [[int(v) for v in t[1:]] for t in tokens]
    return list(list(t) for t in zip(*inputs))


data = get_data()


def count_wins(time: int, distance: int):
    # Only works when time is a even number, which is the case for my inputs
    half = time // 2
    total = half - bisect(
        range(half), distance, key=lambda x: (x * (time - x))
    )
    return total * 2 + 1


first = math.prod(count_wins(t, d) for t, d in data)
time, distance = [int("".join(str(i) for i in d)) for d in zip(*data)]
second = count_wins(time, distance)

print("First:  ", first)
print("Second: ", second)
