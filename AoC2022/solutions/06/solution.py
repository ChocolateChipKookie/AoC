#Advent of Code 2022 day 6
from util import *
YEAR = 2022
DAY = 6


def get_data():
    return input_lines(DAY, YEAR)


data = get_data()[0]

def solve(window_size):
    for i in range(len(data)):
        if len(set(data[i:i+window_size])) == window_size:
            return i + window_size


first = solve(4)
second = solve(14)

print("First:  ", first)
print("Second: ", second)