#Advent of Code 2018 day 22
from util import *
import numpy as np
from queue import PriorityQueue

YEAR = 2018
DAY = 22

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
depth = int(data[0].split()[1])
target = tuple(int(x) for x in data[1].split()[1].split(","))

array_size = 1000, 1000

erosion_levels = np.zeros(array_size, dtype=int)
erosion_levels.fill(-1)


def erosion_level(x, y):
    if erosion_levels[x, y] != -1:
        return erosion_levels[x, y]
    if y == 0 or x == 0:
        value = (x * 16807 + y * 48271 + depth) % 20183
        erosion_levels[x, y] = value
        return value
    value = (erosion_level(x - 1, y) * erosion_level(x, y - 1) + depth) % 20183
    erosion_levels[x, y] = value
    return value


def get_type(x, y):
    return erosion_level(x, y) % 3


erosion_level(*target)
erosion_levels[0, 0] = depth % 20183
erosion_levels[target] = depth % 20183
first = (erosion_levels[:(target[0] + 1), :(target[1] + 1)] % 3).sum()
print("First:  ", first)

visited = set()
queue = PriorityQueue()
queue.put((0, ((0, 0), "T", 0)))

directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]

possible_tools = {
    0: "GT",
    1: "GN",
    2: "TN",
}

tool_transitions = {
    ("GT", "G"): "T",
    ("GT", "T"): "G",

    ("GN", "G"): "N",
    ("GN", "N"): "G",

    ("TN", "T"): "N",
    ("TN", "N"): "T",
}

second = 0
while not queue.empty():
    priority, entry = queue.get()
    pos, tool, distance = entry
    if (pos, tool) in visited:
        continue
    visited.add((pos, tool))
    if pos == target and tool == "T":
        second = distance
        break

    current_terrain = get_type(*pos)
    for d in directions:
        npos = pos[0] + d[0], pos[1] + d[1]
        if npos[0] < 0 or npos[1] < 0:
            continue
        old_terrain = get_type(*pos)
        new_terrain = get_type(*npos)
        cost = 1
        new_tool = tool
        if tool not in possible_tools[new_terrain]:
            cost += 7
            current_tools = possible_tools[old_terrain]
            new_tool = tool_transitions[current_tools, tool]
        new_distance = distance + cost
        h_cost = abs(target[0] - npos[0]) + abs(target[1] - npos[1])
        queue.put((h_cost + new_distance, (npos, new_tool, new_distance)))

print("Second: ", second)
