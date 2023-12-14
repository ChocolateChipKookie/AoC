# Advent of Code 2023 day 14
from util import *

YEAR = 2023
DAY = 14


def get_data():
    return input_array(DAY, YEAR)


def count_load(data: list[list[str]]):
    return sum(
        sum(len(line) - i for i in (i for i, c in enumerate(line) if c == "O"))
        for line in data
    )


def do_step(data: list[list[str]]):
    for row in data:
        next_empty = 0
        for i, c in enumerate(row):
            if c == "#":
                next_empty = i + 1
                continue
            if c == "O":
                if next_empty != i:
                    row[next_empty] = "O"
                    row[i] = "."
                next_empty += 1
                continue
    return data


def array_hash(data):
    return hash("".join("".join(line) for line in data))


first = count_load(do_step(transpose_array(get_data())))

data = get_data()
data = rotate_array(data, clockwise=False)

cycles = 1000000000
c = 0
found = False
last_seen = {}
while c < cycles:
    for d in range(4):
        data = do_step(data)
        data = rotate_array(data, clockwise=True)

    if not found:
        h = array_hash(data)
        if h in last_seen:
            found = True
            period = c - last_seen[h]
            c += (cycles - c) // period * period
        last_seen[array_hash(data)] = c
    c += 1

print("First:  ", first)
print("Second: ", count_load(data))
