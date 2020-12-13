#Advent of Code 2020 day 11
from util import *
import copy
DAY = 11

def get_data():
    d = {'.':-1, "L":0, "#":1}
    return [[d[c] for c in s] for s in input_lines(DAY)]

def print_data(data):
    d = {-1:".", 0:"L", 1:"#"}
    for line in data:
        for val in line:
            print(d[val], end='')
        print()


def get(data, x, y):
    if y < 0 or y >= len(data):
        return 0
    if x < 0 or x >= len(data[0]):
        return 0
    return data[y][x]

data = get_data()

directions = [(-1, -1), (-1, 0), (-1, 1),
              ( 0, -1),          ( 0, 1),
              ( 1, -1), ( 1, 0), ( 1, 1)]

while True:
    new_data = copy.deepcopy(data)
    for y in range(len(data)):
        for x in range(len(data[0])):
            alive = 0
            for direction in directions:
                current = (y + direction[0], x + direction[1])
                val = get(data, current[1], current[0])
                if val == 1:
                    alive += 1

            if data[y][x] == 1 and alive >= 4:
                new_data[y][x] = 0
            if data[y][x] == 0 and alive == 0:
                new_data[y][x] = 1
    if new_data == data:
        break
    data = new_data

first = 0

for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 1:
            first+=1

data = get_data()
while True:
    new_data = copy.deepcopy(data)
    for y in range(len(data)):
        for x in range(len(data[0])):
            alive = 0
            for direction in directions:
                current = (y + direction[0], x + direction[1])
                while True:
                    val = get(data, current[1], current[0])
                    if val == 1:
                        alive += 1
                    if val >= 0:
                        break
                    current = (current[0] + direction[0], current[1] + direction[1])

            if data[y][x] == 1 and alive >= 5:
                new_data[y][x] = 0
            if data[y][x] == 0 and alive == 0:
                new_data[y][x] = 1
    if new_data == data:
        break
    data = new_data

second = 0

for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 1:
            second+=1


print(f"First:  {first}")
print(f"Second: {second}")
