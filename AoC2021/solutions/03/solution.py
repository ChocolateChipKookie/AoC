#Advent of Code 2021 day 3
from util import *
DAY = 3
YEAR = 2021

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()


# First
half_len = len(data)/2
ones_won = [sum(int(x[i]) for x in data) > half_len for i in range(len(data[0]))]
first = int("".join('1' if x else '0' for x in ones_won), 2) * int("".join('0' if x else '1' for x in ones_won), 2)

# Second
most_common = lambda i, data: sum(int(x[i]) for x in data) >= len(data)/2

o2, i = data, 0
while len(o2) > 1:
    ones_won = most_common(i, o2)
    o2 = [x for x in o2 if ones_won ^ (x[i] == '0')]
    i += 1

co2, i = data, 0
while len(co2) > 1:
    zeros_won = not most_common(i, co2)
    co2 = [x for x in co2 if zeros_won ^ (x[i] == '0')]
    i += 1


second = int(o2[0], 2) * int(co2[0], 2)

print(f"First:  {first}")
print(f"Second: {second}")
