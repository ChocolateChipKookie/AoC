#Advent of Code 2021 day 2
from bs4.element import XMLProcessingInstruction
from util import *
DAY = 2
YEAR = 2021

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()

x = sum(int(x.split()[-1]) for x in data if x.startswith("forward"))
y = sum(int(x.split()[-1]) * (-1 if x.startswith("up") else 1) for x in data if not x.startswith("forward"))

first = x * y

x, y, aim = 0, 0, 0

for command, val in (x.split() for x in data):
    val = int(val)
    if command == 'down':
        aim += val
    elif command == 'up':
        aim -= val
    else:
        x += val
        y += val * aim
second = x * y

print(f"First:  {first}")
print(f"Second: {second}")
