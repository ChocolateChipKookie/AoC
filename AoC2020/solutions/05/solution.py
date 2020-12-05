#Advent of Code 2020 day 5
from util import *
import re
DAY = 5

def get_data():
    return input_lines(DAY)

data = get_data()

def get_seat_long(pid):
    # Turn pid to binary
    pid = re.sub(r"[FL]", '0', pid)
    pid = re.sub(r"[BR]", '1', pid)

    # Calculate row
    row = int(pid[0:7], 2)
    # Calculate column
    column = int(pid[7:11], 2)
    # Result
    return row*8+column


def get_seat(pid):
    # Pid is just a binary representation of the seat location
    return int(re.sub(r"[BR]", '1', re.sub(r"[FL]", '0', pid)), 2)

ids = sorted([get_seat(x) for x in data])
first = ids[-1]
second = [x for x in range(ids[0], ids[-1]) if x not in ids][0]

print(f"First:  {first}")
print(f"Second: {second}")
