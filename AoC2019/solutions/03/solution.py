#Advent of Code 2019 day 3
from util import *
DAY = 3


def get_data():
    return input_lines(DAY, 2019)


def positions(line):
    dx = {'L': -1, 'R': 1, 'U': 0, 'D': 0}
    dy = {'L': 0, 'R': 0, 'U': 1, 'D': -1}
    current_position = [0, 0]
    positions = set()
    dist = dict()
    current = 1
    for move in line.split(','):
        for i in range(int(move[1:])):
            current_position[0] += dx[move[0]]
            current_position[1] += dy[move[0]]
            tup = tuple(current_position)
            positions.add(tup)
            if tup not in dist:
                dist[tuple(current_position)] = current
            current += 1
    return positions, dist


data = get_data()

pos1, dist1 = positions(data[0])
pos2, dist2 = positions(data[1])
crossings = pos1 & pos2

location = min(crossings, key=lambda x: dist1[x] + dist2[x])

first = sum(min(crossings, key=lambda x: abs(x[0]) + abs(x[1])))
second = dist1[location] + dist2[location]

print(f"First:  {first}")
print(f"Second: {second}")
