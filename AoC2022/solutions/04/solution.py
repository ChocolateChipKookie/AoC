#Advent of Code 2022 day 4
from util import *
YEAR = 2022
DAY = 4


def get_data():
    return input_lines(DAY, YEAR)


def parse_range(range):
    return tuple(int(i) for i in range.split("-"))


def contains(r1, r2):
    if (r1[1] - r1[0]) < (r2[1] - r2[0]):
        r1, r2 = r2, r1
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def overlaps(r1, r2):
    return r1[0] <= r2[1] and r2[0] <= r1[1]


data = get_data()
ranges = [tuple(parse_range(r) for r in x.split(",")) for x in data]

first = sum(1 for r1, r2 in ranges if contains(r1, r2))
second = sum(1 for r1, r2 in ranges if overlaps(r1, r2))

print("First:  ", first)
print("Second: ", second)
