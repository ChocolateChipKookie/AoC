#Advent of Code 2018 day 6
from util import *
DAY = 6
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

def m_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


data = get_data()
data = [tuple(int(y) for y in x.split(', ')) for x in data]
offset = min(x[0] for x in data), min(x[1] for x in data)
data = [(x[0]-offset[0], x[1]-offset[1]) for x in data]

size = max(x[0] for x in data), max(x[1] for x in data)
closest = [[0] * size[1] for _ in range(size[0])]

for y in range(size[1]):
    for x in range(size[0]):
        distances = sorted([(i, m_dist((x, y), data[i])) for i in range(len(data))], key=lambda i: i[1])
        if distances[0][1] != distances[1][1]:
            closest[x][y] = distances[0][0]
        else:
            closest[x][y] = False

infinite = set(closest[0] + closest[-1] + [x[0] for x in closest] + [x[-1] for x in closest])

count = [0] * len(data)
for y in closest:
    for x in y:
        if x:
            count[x] += 1

count = [count[i] for i in range(len(data)) if i not in infinite]
first = max(count)

MAX_DIST = 10000
offset = MAX_DIST // len(data)
data = [(x[0] + offset, x[1] + offset) for x in data]
size = size[0] + 2*offset, size[1] + 2*offset
dist_sum = [[0] * size[1] for _ in range(size[0])]

for y in range(size[1]):
    for x in range(size[0]):
        dist_sum[x][y] = sum(m_dist((x, y), data[i]) for i in range(len(data)))

second = sum(sum(1 for x in y if x < MAX_DIST) for y in dist_sum)

print(f"First:  {first}")
print(f"Second: {second}")
