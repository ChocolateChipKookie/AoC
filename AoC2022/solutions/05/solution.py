#Advent of Code 2022 day 5
import copy

from util import *
YEAR = 2022
DAY = 5


def get_data():
    return get_input(DAY, YEAR).split('\n')


data = get_data()
stacks = []
while True:
    line = data.pop(0)
    if "[" not in line:
        data.pop(0)
        break
    for stack, i in enumerate(range(1, len(line), 4)):
        while stack >= len(stacks):
            stacks.append([])
        if line[i].isalpha():
            stacks[stack].insert(0, line[i])

commands = (line.split() for line in data)
commands = [tuple(int(i) for i in (t[1], t[3], t[5])) for t in commands]
data = copy.deepcopy(stacks)


def move_one(source, destination):
    stacks[destination].append(stacks[source].pop())


def move_multiple(count, source, destination):
    stacks[destination].extend(stacks[source][-count:])
    stacks[source] = stacks[source][:-count]


for count, src, dest in commands:
    for _ in range(count):
        move_one(src - 1, dest - 1)

first = "".join(s.pop() for s in stacks)

stacks = data
for count, src, dest in commands:
    move_multiple(count, src - 1, dest - 1)

second = "".join(s.pop() for s in stacks)

print("First:  ", first)
print("Second: ", second)