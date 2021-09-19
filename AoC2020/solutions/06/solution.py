#Advent of Code 2020 day 6
from util import *
DAY = 6
YEAR = 2020


def get_data():
    return get_input(DAY, YEAR).strip().split('\n\n')


def solution():
    data = get_data()
    groups = [set("".join(x.split())) for x in data]        # Checks for number of unique elements in a group
    members = [[set(y) for y in x.split()] for x in data]   # Check the number of unique elements per person in a group
    intersect = [j[0].intersection(*j) for j in members]    # Looks for number of unique elements in itersection of group
    first = sum(len(x) for x in groups)
    second = sum(len(x) for x in intersect)

    print(f"First:  {first}")
    print(f"Second: {second}")

solution()
