#Advent of Code 2020 day 9
from util import *
DAY = 9

def get_data():
    return [int(x) for x in input_lines(DAY)]

data = get_data()

first = None
data_range = 25



def solution():
    for i in range(data_range, len(data)):
        s = data[i-data_range:i]
        res = []
        for x in s:
            for y in s:
                if x != y:
                    res.append(x + y)

        if data[i] not in res:
            first = data[i]
            break

    second = None
    for i in range(len(data) - 1):
        sum = 0
        for j in range(i, len(data) - 1):
            sum += data[j]
            if sum > first:
                break
            if sum == first:
                d = sorted([data[x] for x in range(i, j+1)])
                second = d[0] + d[-1]
                break
        if second:
            break

    print(f"First:  {first}")
    print(f"Second: {second}")

solution()