# Advent of Code 2023 day 13
from util import *

YEAR = 2023
DAY = 13


def get_data():
    result = [[]]
    for line in input_lines(DAY, YEAR):
        if not line:
            result.append([])
            continue
        result[-1].append([c for c in line])
    return result


def compare(h1, h2, smudges):
    z = zip(h1, h2)
    diff = sum(sum(1 for c1, c2 in zip(l1, l2) if c1 != c2) for l1, l2 in z)
    return diff == smudges


def get_reflection(array, smudges):
    for i in range(len(array) - 1):
        if compare(array[i::-1], array[i + 1 :], smudges):
            return i + 1


def bidirectional(array, smudges=0):
    res = get_reflection(array, smudges)
    if res is not None:
        return res * 100
    arr = [list(z) for z in zip(*array)]
    res = get_reflection(arr, smudges)
    assert res is not None
    return res


data = get_data()
first = sum(bidirectional(a) for a in data)
second = sum(bidirectional(a, 1) for a in data)

print("First:  ", first)
print("Second: ", second)
