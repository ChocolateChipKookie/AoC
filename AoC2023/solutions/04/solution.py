#Advent of Code 2023 day 4
from util import *
YEAR = 2023
DAY = 4

def get_data() -> list[tuple[set[str], set[str]]]:
    lines = input_lines(DAY, YEAR)
    def parse_side(s) -> set[str]:
        return set(s.strip().split())
    sides = [t.split("|") for t in lines]
    sets = [(parse_side(l), parse_side(r)) for l, r in sides]
    return sets

data = get_data()
wins = [len(l.intersection(r)) for l, r in data]

def total_result(index, cache):
    if index in cache:
        return cache[index]

    res = 1
    if wins[index] > 0:
        low_bound = index + 1
        up_bound = min(low_bound + wins[index], len(wins))
        res += sum(total_result(i, cache) for i in range(low_bound, up_bound))
    cache[index] = res
    return res

first = sum((2 ** (w - 1)) for w in wins if w > 0)
second = sum(total_result(r, {}) for r in range(len(wins)))

print("First:  ", first)
print("Second: ", second)
