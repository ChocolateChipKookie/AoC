
#Advent of Code 2020 day 13
from util import *
import math
DAY = 13
YEAR = 2020


def first():
    data = input_integers(DAY, YEAR)
    timepoint, data = data[0], data[1:]

    min_bus = min(data)
    min_wait = min_bus
    for bus in data:
        prev_bus = timepoint // bus * bus
        wait = prev_bus + bus - timepoint
        if wait < min_wait:

            min_wait = wait
            min_bus = bus
    return min_bus * min_wait


def second():
    data = input_lines(DAY)[1].split(',')
    data = [(x[0], int(x[1])) for x in enumerate(data) if x[1] != 'x']

    current_loop = 1
    current_base = 0
    for i, prime in data:
        for n in range(prime):
            if (current_base + current_loop * n + i) % prime == 0:
                current_base += current_loop * n
                current_loop *= prime
                break
    return current_base



print(f"First:  {first()}")
print(f"Second: {second()}")
