#Advent of Code 2018 day 3
from util import *
DAY = 3
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()

pieces = []
for line in data:
    line = line[1:]
    tokens = line.split()
    id = int(tokens[0])
    pos = [int(x) for x in tokens[2][:-1].split(',')]
    size = [int(x) for x in tokens[3].split('x')]
    pieces.append((id, pos, size))

coords = dict()
for piece in pieces:
    pos, size = piece[1:]
    for x in range(size[0]):
        for y in range(size[1]):
            coord = (pos[0] + x, pos[1] + y)
            coords[coord] = coords.get(coord, 0) + 1

first = len(coords) - [coords[x] for x in coords].count(1)
second = None

for piece in pieces:
    id, pos, size = piece
    is_whole = True
    for x in range(size[0]):
        for y in range(size[1]):
            coord = (pos[0] + x, pos[1] + y)
            if coords[coord] > 1:
                is_whole = False
    if is_whole:
        second = id
        break

print(f"First:  {first}")
print(f"Second: {second}")
