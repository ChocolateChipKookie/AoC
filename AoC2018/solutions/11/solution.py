#Advent of Code 2018 day 11
from util import *
DAY = 11
YEAR = 2018


def get_data():
    return input_lines(DAY, YEAR)


serial_number = int(get_data()[0])

dimensions = (300, 300)
grid = [[0] * (dimensions[1] + 1) for _ in range(dimensions[0] + 1)]

def value(x, y, serial_number):
    id = x + 10
    pl = id * y
    pl += serial_number
    pl *= id
    pl = (pl // 100) % 10
    return pl - 5

for y in range(1, dimensions[1] + 1):
    for x in range(1, dimensions[0] + 1):
        val = value(x, y, serial_number)
        partial_sum = grid[x-1][y] + grid[x][y-1] - grid[x-1][y-1] + val
        grid[x][y] = partial_sum


def get_value(x, y, size):
    return grid[x + size][y + size] - grid[x + size][y] - grid[x][y + size] + grid[x][y]


def find_largest(size):
    pos = (0, 0)
    total = 0
    for y in range(1, dimensions[1] - size + 1):
        for x in range(1, dimensions[0] - size + 1):
            t = get_value(x, y, size)
            if t > total:
                total = t
                pos = (x+1, y+1)
    return pos, size, total


first = find_largest(3)[0]
second = ((0, 0), 0, 0)

for i in range(20):
    largest = find_largest(i)
    if largest[2] > second[2]:
        second = largest
second = (*second[0], second[1])

print(f"First:  {first}")
print(f"Second: {second}")
