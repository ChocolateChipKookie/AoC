# Advent of Code 2023 day 10
from util import *

YEAR = 2023
DAY = 10


def get_data() -> list[list[str]]:
    lines = input_lines(DAY, YEAR)
    mapping = [[c for c in line] for line in lines]
    return list(list(t) for t in zip(*mapping))


def get_value(x: int, y: int) -> str:
    return pipe_map[x][y]


def get_neighbours(x: int, y: int, val: str) -> list[tuple[int, int]]:
    move = {
        "|": [(0, -1), (0, 1)],
        "-": [(-1, 0), (1, 0)],
        "L": [(0, -1), (1, 0)],
        "J": [(0, -1), (-1, 0)],
        "7": [(0, 1), (-1, 0)],
        "F": [(0, 1), (1, 0)],
        "S": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    }

    if val not in move:
        return []

    def gen():
        for dx, dy in move[val]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(pipe_map) and 0 <= ny < len(pipe_map[0]):
                yield nx, ny

    return list(gen())


def get_start() -> tuple[int, int]:
    for x, column in enumerate(pipe_map):
        for y, value in enumerate(column):
            if value == "S":
                return x, y
    return 0, 0


def explore_loop(
    start: tuple[int, int], current: tuple[int, int]
) -> dict[tuple[int, int], str] | None:
    path = {
        start: "S",
    }
    previous = start
    first = current
    while True:
        val = get_value(*current)
        if val == "S":
            break

        neighbours = get_neighbours(*current, val)
        if previous not in neighbours:
            return None

        path[current] = val
        previous, current = current, next(
            x for x in neighbours if x != previous
        )
    last = previous

    for c in "|-LJ7F":
        if set(get_neighbours(*start, c)) == {first, last}:
            path[start] = c
            break

    return path


def get_loop() -> dict[tuple[int, int], str]:
    x, y = get_start()
    start_neighbours = get_neighbours(x, y, "S")

    for sn in start_neighbours:
        res = explore_loop((x, y), sn)
        if res:
            return res
    return {}


def is_inside_loop(loop, pos) -> bool:
    # Part of loop is automatically not inside
    if pos in loop:
        return False

    # Count number of crossings across the loop from (x, 0) to pos
    crossings = 0
    corner = None
    for y in range(pos[1]):
        test_pos = pos[0], y
        val = loop.get(test_pos, ".")

        if corner:
            # F     7
            # | and | are considered to be one long crossing
            # J     L
            #
            #       F     7
            # while | and | are 2 separate crossings
            #       L     J
            if (corner, val) in {("7", "J"), ("F", "L")}:
                crossings += 1
            if val in "LJ":
                corner = None
            continue
        if val in "7F":
            corner = val
            crossings += 1
            continue
        if val == "-":
            crossings += 1
            continue
    return crossings % 2 == 1


def get_tiles_in_loop() -> int:
    loop = get_loop()
    width = len(pipe_map)
    height = len(pipe_map[0])

    total = 0
    for x in range(1, width):
        for y in range(1, height):
            if is_inside_loop(loop, (x, y)):
                total += 1
    return total


pipe_map = get_data()

first = len(get_loop()) // 2
second = get_tiles_in_loop()

print("First:  ", first)
print("Second: ", second)
