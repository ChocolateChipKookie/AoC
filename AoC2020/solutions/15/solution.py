#Advent of Code 2020 day 15
from util import *
DAY = 15
YEAR = 2020


def get_data():
    return input_lines(DAY, YEAR)

data = get_data()

def run(iterations):
    data = input_integers(DAY)
    memory = { x[1]: x[0] + 1 for x in enumerate(data[:-1])}
    last = data[-1]

    for iter in range(len(data), iterations):
        if last not in memory:
            memory[last] = iter
            last = 0
        else:
            diff = iter - memory[last]
            memory[last] = iter
            last = diff

    return last


def first():
    return run(2020)


def second():
    return run(30000000)


print(f"First:  {first()}")
print(f"Second: {second()}")
