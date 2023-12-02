#Advent of Code 2023 day 2
from util import *
from math import prod
YEAR = 2023
DAY = 2

def get_data():
    return input_lines(DAY, YEAR)


def parse(game):
    def parse_dice(d: str):
        n, color = d.split()
        return color, int(n)
    desc, sets_str = game.split(":")
    id = int(desc.split()[1])
    sets = [[parse_dice(dice.strip()) for dice in s.split(",")]
                                      for s in sets_str.split(";")]
    return id, sets

def is_possible(game: str):
    id, sets = parse(game)
    possible = all(all(n <= limit[color] for color, n in s) for s in sets)
    return id if possible else 0

def get_power(game: str):
    _, sets = parse(game)

    mins = {"red": 0, "green": 0, "blue": 0}
    for s in sets:
        for color, n in s:
            mins[color] = max([mins.get(color, 0), n])
    return prod(mins.values())

data = get_data()
limit = {"red": 12, "green": 13, "blue": 14}
first = sum(is_possible(d) for d in data)
second = sum(get_power(d) for d in data)

print("First:  ", first)
print("Second: ", second)
