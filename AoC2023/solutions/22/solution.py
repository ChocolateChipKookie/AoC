# Advent of Code 2023 day 22
from util import *
from bisect import bisect

YEAR = 2023
DAY = 22

Position = tuple[int, int, int]


def get_data() -> list[list[Position]]:
    bricks = []
    for line in input_lines(DAY, YEAR):
        l, r = line.split("~")
        start = tuple(int(i) for i in l.split(","))
        end = tuple(int(i) for i in r.split(","))
        bricks.append([])
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    bricks[-1].append((x, y, z))
        bricks[-1].sort(key=lambda p: p[-1])
    bricks.sort(key=lambda b: b[0][-1])
    return bricks


def calculate_supports():
    def move(part: Position, dz: int) -> Position:
        return *part[:2], part[2] - dz

    def intersects(brick, dz) -> tuple[bool, list[int]]:
        if brick[0][-1] == dz:
            return True, []
        intersection = set()
        for part in brick:
            pos = move(part, dz)
            i = all_spaces.get(pos, None)
            if i is not None:
                intersection.add(i)
        return bool(intersection), list(intersection)

    all_spaces: dict[Position, int] = {}
    supported_by: dict[int, list[int]] = {}

    for index, brick in enumerate(data):
        for dz in range(brick[0][-1] + 1):
            found, others = intersects(brick, dz)
            if found:
                supported_by[index] = others
                for part in brick:
                    pos = move(part, dz - 1)
                    all_spaces[pos] = index
                break
    return supported_by


data = get_data()
supported_by = calculate_supports()
supports = {}
for k, v in supported_by.items():
    for val in v:
        if val not in supports:
            supports[val] = []
        supports[val].append(k)

def is_removable(i):
    return all(len(v) > 1 for v in supported_by.values() if i in v)


first = sum(1 for i in supported_by if is_removable(i))

cache = {}
def chain(i):
    if i not in supports:
        return 0
    removed = set([i])
    not_removed = set()
    to_check = list(supports[i])
    while to_check:
        current = to_check.pop(0)
        if all(s in removed for s in supported_by[current]):
            if current in cache:
                r, nr = cache[current]
                removed.update(r)
                to_check.extend(nr)
                to_check.sort(key=lambda p: data[p][0][-1])
                continue
            removed.add(current)
            for i in supports.get(current, []):
                index = bisect(to_check, data[i][0][-1], key=lambda p: data[p][0][-1])
                to_check.insert(index, i)
        else:
            not_removed.add(current)
    cache[i] = removed, not_removed
    return len(removed) - 1

second = sum(chain(i) for i in range(len(data) -1, -1, -1))

print("First:  ", first)
print("Second: ", second)
