#Advent of Code 2022 day 16
import dataclasses
from copy import deepcopy

from util import *
YEAR = 2022
DAY = 16


def get_data():
    return input_lines(DAY, YEAR)


def parse_valve(valve_str: str):
    tokens = valve_str.split()
    valve = tokens[1]
    rate = int(tokens[4].split('=')[1][:-1])
    tunnels = tuple(t[:2] for t in tokens[9:])
    return valve, rate, tunnels



data = get_data()
valves = {v: (r, t) for v, r, t in (parse_valve(v) for v in data)}


distances = {}


def get_dist(start, end):
    if start > end:
        start, end = end, start
    return distances[start, end]


def add_dist(start, end, dist):
    if start > end:
        start, end = end, start
    distances[start, end] = dist


def map_distances(start, end):
    global distances

    visited = set()
    queue = [(start, 0)]
    while queue:
        current, d = queue.pop(0)
        visited.add(current)
        add_dist(start, current, d)
        if current == end:
            break
        for neighbour in valves[current][1]:
            if neighbour in visited:
                continue
            queue.append((neighbour, d + 1))

valid_valves = set(v for v in valves if valves[v][0] != 0)
valid_distances = {}
for v1 in valid_valves:
    for v2 in valid_valves:
        if v1 == v2:
            continue
        map_distances(v1, v2)
        dist = get_dist(v1, v2)
        valid_distances[(v1, v2)] = dist
        valid_distances[(v2, v1)] = dist

for v1 in valid_valves:
    dist = get_dist(v1, "AA")
    valid_distances[("AA", v1)] = dist



def depth_search(current_valve: str, time_left: int, opened_valves: set):
    if time_left <= 0:
        return 0
    best = 0
    for valve in valid_valves:
        if current_valve == valve:
            continue
        if valve not in opened_valves:
            at_opening = time_left - valid_distances[current_valve, valve] - 1
            if at_opening <= 0:
                continue
            pressure = at_opening * valves[valve][0]
            opened_valves.add(valve)
            others = depth_search(valve, at_opening, opened_valves)
            opened_valves.remove(valve)
            best = max(best, pressure + others)

    return best


opened = set()
first = depth_search("AA", 30, opened)
print("First:  ", first)

@dataclasses.dataclass
class Actor:
    name: str
    valve: str = "AA"
    timeout = 0


def timed_search(human: Actor, elephant: Actor, time_left: int, opened_valves: set):
    if time_left <= 0 or len(opened) == len(valid_valves):
        return 0

    if human.timeout > 0 and elephant.timeout > 0:
        jump = min(human.timeout, elephant.timeout)
        human.timeout -= jump
        elephant.timeout -= jump
        return timed_search(human, elephant, time_left - jump, opened_valves)

    best = 0

    for actor in [human, elephant]:
        if actor.timeout != 0:
            continue
        current_valve = actor.valve

        h_v, h_t = human.valve, human.timeout
        e_v, e_t = elephant.valve, elephant.timeout

        for valve in valid_valves:
            if actor.valve == valve:
                continue
            if valve not in opened_valves:
                distance = valid_distances[current_valve, valve]
                actor.timeout = distance + 1
                at_release = time_left - actor.timeout
                if at_release <= 0:
                    continue

                opened_valves.add(valve)
                pressure = valves[valve][0] * at_release
                actor.valve = valve
                score = timed_search(human, elephant, time_left, opened_valves)
                human.valve, human.timeout = h_v, h_t
                elephant.valve, elephant.timeout = e_v, e_t
                opened_valves.remove(valve)
                best = max(best, pressure + score)
        break

    return best


human = Actor(name="Human")
elephant = Actor(name="Elephant")
second = timed_search(human, elephant, 26, opened)

print("Second: ", second)
