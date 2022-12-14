#Advent of Code 2022 day 13
from util import *
from functools import cmp_to_key
YEAR = 2022
DAY = 13


def get_data():
    return input_lines(DAY, YEAR)


def compare(e1, e2):
    if isinstance(e1, int) and isinstance(e2, int):
        if e1 == e2:
            return 0
        return -1 if e1 < e2 else 1

    if isinstance(e1, list) and isinstance(e2, list):
        for i1, i2 in zip(e1, e2):
            result = compare(i1, i2)
            if abs(result) > 0:
                return result
        if len(e1) == len(e2):
            return 0
        return -1 if len(e1) < len(e2) else 1

    def to_list(item):
        if isinstance(item, list):
            return item
        return [item]
    return compare(to_list(e1), to_list(e2))


data = get_data()
lists = [eval(x) for x in data if x.strip()]
pairs = [t for t in zip(lists[0::2], lists[1::2])]

first = sum(i for i, pair in enumerate(pairs, 1) if compare(*pair) < 0)
drivers = ([[2]], [[6]])
lists.extend(drivers)
lists.sort(key=cmp_to_key(compare))
second = (lists.index(drivers[0]) + 1) * (lists.index(drivers[1]) + 1)

print("First:  ", first)
print("Second: ", second)