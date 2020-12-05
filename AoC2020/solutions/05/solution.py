#Advent of Code 2020 day 5
from util import *
DAY = 5

def get_data():
    return input_lines(DAY)

data = get_data()

def get_seat_long(pid):
    # Turn pid to binary
    pid = pid.replace("F", "0")
    pid = pid.replace("B", "1")
    pid = pid.replace("L", "0")
    pid = pid.replace("R", "1")

    # Calculate row
    row = int(pid[0:7], 2)
    # Calculate column
    column = int(pid[7:11], 2)
    # Result
    return row*8+column


def get_seat(pid):
    # Pid is just a binary representation of the seat location
    return int(pid.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)

ids = sorted([get_seat(x) for x in data])
first = ids[-1]
second = [x for x in range(ids[0], ids[-1]) if x not in ids][0]

print(f"First:  {first}")
print(f"Second: {second}")
