#Advent of Code 2020 day 3
from util import *
import numpy
DAY = 3

def get_data():
    return input_lines(DAY)

def solution():
    data = get_data()

    def find_trees(data, slope):
        pos = [0, 0]
        result = 0
        while pos[0] < len(data):
            if data[pos[0]][pos[1] % len(data[0])] == "#":
                result += 1
            for x in range(2):
                pos[x] += slope[x]
        return result

    first = find_trees(data, (1, 3))

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    second = numpy.prod([find_trees(data, slope) for slope in slopes])

    print(f"First:  {first}")
    print(f"Second: {second}")

def golf():
    d = get_data()
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    sol = list(sum(1 for y in range(len(d)) if y * s[0] < len(d) and d[y*s[0]][y*s[1]%len(d[0])]=='#') for s in slopes)
    print(f"First:  {sol[1]}")
    print(f"Second: {numpy.prod(sol)}")

    """
        sol = 
        list(
            sum( 1 for y in range(len(d)) if                                # Count if condition is satisfied
                    y * s[0] < len(d) and d[y*s[0]][y*s[1]%len(d[0])]=='#'  # Condition: y < height && data[y * dy][(y * dx) % width] == tree
            ) for s in slopes)                                              # For every slope
        
        print(f"First:  {sol[1]}")
        print(f"Second: {numpy.prod(sol)}")
    """



golf()