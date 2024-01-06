# Advent of Code 2023 day 12
from util import *

YEAR = 2023
DAY = 12


def get_data():
    data = [t.split() for t in input_lines(DAY, YEAR)]
    return [
        (l.replace(".", " "), [int(t) for t in r.split(",")]) for l, r in data
    ]


cache = {}


def count_valid(springs: str, lengths: list[int]):
    cached = cache.get((springs, tuple(lengths)), None)
    if cached is not None:
        return cached

    if not lengths:
        return 0 if "#" in springs else 1

    if sum(lengths) + len(lengths) - 1 > len(springs):
        return 0

    if len(lengths) == 1 and "#" not in springs:
        length = lengths[0]
        if length == 1:
            return springs.count("?")
        others = (len(s) for s in springs.split())
        return sum(l - length + 1 for l in others if l >= length)

    target = max(lengths)
    indices = [i for i, t in enumerate(lengths) if t == target]

    pivot = indices[len(indices) // 2]
    current_len = lengths[pivot]
    total = 0

    for begin in range(len(springs) - current_len + 1):
        end = begin + current_len
        is_valid = all(c in "#?" for c in springs[begin:end])
        if not is_valid:
            continue
        if begin != 0 and springs[begin - 1] == "#":
            continue
        if end != len(springs) and springs[end] == "#":
            continue

        left = count_valid(
            springs[: max(0, begin - 1)].strip(), lengths[:pivot]
        )
        if not left:
            continue
        right = count_valid(
            springs[min(len(springs), end + 1) :].strip(), lengths[pivot + 1 :]
        )
        total += left * right

    cache[springs, tuple(lengths)] = total
    return total


data = get_data()

first = sum(count_valid(*d) for d in data)
second = sum(count_valid("?".join([s] * 5), d * 5) for s, d in data)

print("First:  ", first)
print("Second: ", second)
