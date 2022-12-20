#Advent of Code 2022 day 20
from util import *
YEAR = 2022
DAY = 20

def get_data():
    return [int(x.strip()) for x in input_lines(DAY, YEAR)]


data = get_data()


def apply_move(position, shift, values: list):
    new_position = (position + shift) % (len(values) - 1)
    val = values.pop(position)
    values.insert(new_position, val)


def decrypt(data, key=1, mixes=1):
    for i in range(len(data)):
        data[i] *= key

    indexes = [i for i in range(len(data))]
    for mix in range(mixes):
        for i in range(len(data)):
            position = indexes.index(i)
            shift = data[position]
            apply_move(position, shift, data)
            apply_move(position, shift, indexes)

    zero_index = data.index(0)
    coordinate_indexes = [1000, 2000, 3000]
    coordinate_indexes = [(zero_index + ci) % len(data) for ci in coordinate_indexes]
    values = [data[ci] for ci in coordinate_indexes]
    return sum(values)


first = decrypt(get_data())
second = decrypt(get_data(), 811589153, 10)

print("First:  ", first)
print("Second: ", second)