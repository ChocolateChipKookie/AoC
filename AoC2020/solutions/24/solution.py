#Advent of Code 2020 day 24
from util import *
DAY = 24

def get_data():
    lines = input_lines(DAY)
    def parse_line(line):
        tokens = []
        while len(line) != 0:
            if line[0:1] in 'ew':
                tokens.append(line[0:1])
                line = line[1:]
            else:
                tokens.append(line[0:2])
                line = line[2:]
        return tokens

    return [parse_line(line) for line in lines]


data = get_data()
moves = {'e':(1, 0), 'w':(-1, 0), 'se':(1, -1), 'nw':(-1, 1), 'sw':(0, -1), 'ne':(0, 1)}
directions = ['e', 'w', 'se', 'nw', 'sw', 'ne']

tiles = {}
for tile in data:
    pos = [0, 0]
    for move in tile:
        m = moves[move]
        pos[0] += m[0]
        pos[1] += m[1]
    pos = tuple(pos)
    if pos in tiles:
        tiles[pos] = not tiles[pos]
    else:
        tiles[pos] = True

first = sum(1 for tile in tiles if tiles[tile])


def get_tile(pos):
    if pos in tiles:
        return tiles[pos]
    return False


def get_neighbors(pos):
    neighbours = []
    for direction in directions:
        move = moves[direction]
        neighbours.append((pos[0] + move[0], pos[1] + move[1]))
    return neighbours


for iter in range(100):
    new_tiles = {}
    flipped = set()

    for tile in tiles:
        to_update = [tile] + get_neighbors(tile)

        for pos in to_update:
            if pos in flipped:
                continue
            flipped.add(pos)
            count = sum(1 for neighbor in get_neighbors(pos) if get_tile(neighbor))
            current = get_tile(pos)
            if current:
                new_tiles[pos] = not (count == 0 or count > 2)
            else:
                new_tiles[pos] = count == 2

    tiles = {pos:True for pos in new_tiles if new_tiles[pos]}

second = sum(1 for tile in tiles if tiles[tile])

print(f"First:  {first}")
print(f"Second: {second}")
