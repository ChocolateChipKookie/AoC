#Advent of Code 2021 day 1
from util import *
DAY = 1
YEAR = 2021

def get_data():
    return [int(x.strip()) for x in input_lines(DAY, YEAR)]

data = get_data()

first = sum(1 for x, y in zip(data[:-1], data[1:]) if x < y)

sliding = [sum(data[i:i+3]) for i in range(len(data)-2)]
second = sum(1 for x, y in zip(sliding[:-1], sliding[1:]) if x < y)

print(f"First:  {first}")
print(f"Second: {second}")
