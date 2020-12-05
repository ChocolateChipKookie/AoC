#Advent of Code 2020 day 5
from util import *
import re
DAY = 5


def get_data():
    return input_lines(DAY)


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


def solution():
    data = get_data()

    ids = sorted([get_seat(x) for x in data])
    first = ids[-1]
    second = next(filter(lambda x: x not in ids, range(ids[0], ids[-1])))

    print(f"First:  {first}")
    print(f"Second: {second}")


def golf():
    d = input_lines(DAY)
    i = {int(x.translate("".maketrans("FBLR", "0101")), 2) for x in d}
    print(f"First:  {max(i)}")
    print(f"Second: {min(set(range(min(i), max(i)))-i)}")


solution()
golf()

