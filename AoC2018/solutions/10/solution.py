#Advent of Code 2018 day 10
from util import *
DAY = 10
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
data = [x.split("=<") for x in data]
data = [(x[1].split(">")[0].split(), x[2][:-1].split()) for x in data]
data = [((int(x[0][0][:-1]), int(x[0][1])), (int(x[1][0][:-1]), int(x[1][1]))) for x in data]

def bounding_box(data):
    bb = [*data[0][0], *data[0][0]]
    for point, _ in data:
        bb[0] = min(bb[0], point[0])
        bb[1] = min(bb[1], point[1])
        bb[2] = max(bb[2], point[0])
        bb[3] = max(bb[3], point[1])
    return bb

def step(data):
    new_data = []
    for point, speed in data:
        new_data.append(((point[0] + speed[0], point[1] + speed[1]), speed))
    return new_data

def print_constellation(data):
    bb = bounding_box(data)
    res = [["."] * (bb[2] - bb[0] + 1) for _ in range(bb[3] - bb[1] + 1)]

    for point, _ in data:
        res[point[1] - bb[1]][point[0] - bb[0]] = "#"

    for line in res:
        print("".join(line))


prev_bb = bounding_box(data)
prev_size = (prev_bb[2] - prev_bb[0], prev_bb[3] - prev_bb[1])
counter = 0

while True:
    new_data = step(data)
    new_bb = bounding_box(new_data)
    new_size = (new_bb[2] - new_bb[0], new_bb[3] - new_bb[1])
    if new_size[0] > prev_size[0] or new_size[1] > prev_size[1]:
        break
    data = new_data
    prev_size = new_size
    counter += 1


first = ""
second = counter

print(f"First:  {first}")
print_constellation(data)
print(f"Second: {second}")
