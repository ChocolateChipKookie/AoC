# Advent of Code 2023 day 18
from util import *

YEAR = 2023
DAY = 18


def get_data():
    data = [
        (d, int(l), h[2:-1])
        for d, l, h in [d.split() for d in input_lines(DAY, YEAR)]
    ]
    first = [(d, l) for d, l, _ in data]

    def parse_hex(h):
        direction = "RDLU"[int(h[-1])]
        num = int(h[:-1], base=16)
        return direction, num

    second = [parse_hex(h) for _, _, h in data]
    return first, second


directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def calc_volume(data):
    points = []
    current = (0, 0)
    edges = 0
    for d, l in data:
        points.append(current)
        dx, dy = directions[d]
        edges += l
        current = current[0] + dx * l, current[1] + dy * l

    area = 0
    for i, p1 in enumerate(points):
        p2 = points[(i + 1) % len(points)]
        area += p1[0] * p2[1]
        area -= p1[1] * p2[0]
    return abs(area // 2) + edges // 2 + 1


data1, data2 = get_data()

first = calc_volume(data1)
second = calc_volume(data2)

print("First:  ", first)
print("Second: ", second)
