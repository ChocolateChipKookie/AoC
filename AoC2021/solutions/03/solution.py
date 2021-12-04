#Advent of Code 2021 day 3
from util import *
DAY = 3
YEAR = 2021

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()

half_len = len(data)/2
ones_won = [sum(int(x[i]) for x in data) > half_len for i in range(len(data[0]))]
bool_map = {True: '1', False: '0'}

first = int("".join(bool_map[x] for x in ones_won), 2) * int("".join(bool_map[not x] for x in ones_won), 2)

oxy_data, i = data, 0
while len(oxy_data) > 1:
    half_len = len(oxy_data) / 2
    ones_won = sum(int(x[i]) for x in oxy_data) >= half_len
    oxy_data = [x for x in oxy_data if ones_won ^ (x[i] == '0')]
    i += 1

co2_data, i = data, 0
while len(co2_data) > 1:
    half_len = len(co2_data) / 2
    zeros_won = not (sum(int(x[i]) for x in co2_data) >= half_len)
    co2_data = [x for x in co2_data if zeros_won ^ (x[i] == '0')]
    i += 1

oxy = int(oxy_data[0], 2)
co2 = int(co2_data[0], 2)

second = oxy * co2

print(f"First:  {first}")
print(f"Second: {second}")
