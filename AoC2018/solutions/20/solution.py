#Advent of Code 2018 day 20
from util import *
YEAR = 2018
DAY = 20


def get_data():
    return input_lines(DAY, YEAR)


def generate_map(regex):
    regex = regex[1:-1]
    revealed = {(0, 0)}
    directions = {
        "N": ( 0,  1),
        "S": ( 0, -1),
        "E": ( 1,  0),
        "W": (-1,  0),
    }

    def recurse(start_pos):
        nonlocal revealed
        nonlocal regex
        pos = start_pos

        while len(regex) > 0:
            current_char = regex[0]
            regex = regex[1:]
            if current_char in directions:
                d = directions[current_char]
                pos = pos[0] + d[0], pos[1] + d[1]
                revealed.add(pos)
                pos = pos[0] + d[0], pos[1] + d[1]
                revealed.add(pos)
            else:
                if current_char == "(":
                    recurse(pos)
                elif current_char == "|":
                    pos = start_pos
                else:
                    return

    recurse((0, 0))
    return revealed


def flood(revealed_rooms):
    directions = [(0, 1), (0, -1), (1,  0), (-1, 0)]
    to_check = [((0, 0), 0)]
    checked = set()
    distances = []
    while len(to_check) > 0:
        pos, dist = to_check.pop()
        distances.append(dist)
        checked.add(pos)
        for d in directions:
            npos = pos[0] + d[0], pos[1] + d[1]
            if npos in revealed:
                npos = npos[0] + d[0], npos[1] + d[1]
                if npos not in checked:
                    to_check.append((npos, dist + 1))
    return distances


data = get_data()[0]
revealed = generate_map(data)
distances = flood(revealed)

first = max(distances)
second = sum(1 for i in distances if i >= 1000)

print("First:  ", first)
print("Second: ", second)
