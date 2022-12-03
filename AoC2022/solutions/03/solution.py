#Advent of Code 2022 day 3
from util import *
YEAR = 2022
DAY = 3


def get_data():
    return input_lines(DAY, YEAR)


def intersect(data):
    result = set(data[0])
    for d in data[1:]:
        result = result.intersection(set(d))
    return result.pop()


data = get_data()

priorities = {}
for i in range(26):
    priorities[chr(i + ord("a"))] = i + 1
    priorities[chr(i + ord("A"))] = i + 27

side_len = ((d, len(d)//2) for d in data)
intersections = (intersect((s[:l], s[l:])) for s, l in side_len)
first = sum(priorities[i] for i in intersections)

groups = [data[i:i+3] for i in range(0, len(data), 3)]
intersections = (intersect(group) for group in groups)
second = sum(priorities[i] for i in intersections)

print("First:  ", first)
print("Second: ", second)