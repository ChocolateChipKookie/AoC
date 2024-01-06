# Advent of Code 2023 day 23
from util import *
import sys

sys.setrecursionlimit(50000)

YEAR = 2023
DAY = 23


def get_data():
    return input_array(DAY, YEAR)


hiking_map = get_data()
distances = {}

Position = tuple[int, int]

neighbours = {
    (0, 1): "v",
    (0, -1): "^",
    (1, 0): ">",
    (-1, 0): "<",
}


def create_graph(ignore_slopes: bool = False):
    nodes = [start, end]

    def is_path(x, y, slope=None):
        val = hiking_map[y][x]
        if slope is None or ignore_slopes:
            return val != "#"
        return val == "." or val == slope

    for y, line in enumerate(hiking_map[1:-1], 1):
        for x, c in enumerate(line[1:-1], 1):
            if c == "#":
                continue
            if sum(1 for dx, dy in neighbours if is_path(x + dx, y + dy)) > 2:
                nodes.append((x, y))

    result = {}
    for node in nodes:
        result[node] = {}
        for (dx, dy), c in neighbours.items():
            previous = node
            current = previous[0] + dx, previous[1] + dy
            if not (0 <= current[1] < len(hiking_map)):
                continue
            if not is_path(*current, c):
                continue

            length = 1
            while current not in nodes:
                for (dx, dy), c in neighbours.items():
                    pos = current[0] + dx, current[1] + dy
                    if pos == previous:
                        continue
                    if is_path(*pos, c):
                        length += 1
                        previous, current = current, pos
                        break
                else:
                    length = None
                    break
            if length is not None:
                result[node][current] = length
    return result


def get_max_path(current, visited=None, total: int = 0):
    if visited is None:
        visited = set()
    if current == end:
        return total
    result = 0
    visited.add(current)
    for neighbour, distance in graph[current].items():
        if neighbour in visited:
            continue
        result = max(
            result, get_max_path(neighbour, visited, total + distance)
        )
    visited.remove(current)
    return result


start = "".join(hiking_map[0]).find("."), 0
end = "".join(hiking_map[-1]).find("."), len(hiking_map) - 1

graph = create_graph(False)
first = get_max_path(start)
graph = create_graph(True)
second = get_max_path(start)
print("First:  ", first)
print("Second: ", second)
