#Advent of Code 2022 day 10
from util import *
YEAR = 2022
DAY = 10

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
tokens = [d.split() for d in data]
commands = [((t[0],) if len(t) == 1 else (t[0], int(t[1]))) for t in tokens]

cycles = {
    "addx": 2,
    "noop": 1
}

reg = 1
cycle = 0

volumes = []


def advance_cycles(n):
    global cycle
    global volumes
    for _ in range(n):
        volumes.append(reg)
    cycle += n


for command in commands:
    advance_cycles(cycles[command[0]])
    if command[0] == "addx":
        reg += command[1]

checkpoints = [20, 60, 100, 140, 180, 220]
first = 0
for checkpoint in checkpoints:
    volume = volumes[checkpoint - 1]
    first += checkpoint * volume

print("First:  ", first)
print("Second: ")

row_len = 40
for i in range(0, len(volumes), row_len):
    row = volumes[i:i + row_len]
    result = []
    for j, vol in enumerate(row):
        in_range = abs(j - vol) <= 1
        result.append("#" if in_range else " ")
    print("".join(result))


