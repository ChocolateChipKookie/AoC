#Advent of Code 2020 day 14
from util import *
DAY = 14

def get_data():
    return input_lines(DAY)


def first():
    data = get_data()
    res = {}
    mask1 = []
    mask0 = []
    for line in data:
        if line[0:4] == 'mask':
            mask = line.split(' = ')[1]
            mask0 = []
            mask1 = []
            for i in range(0, 36):
                if mask[i] == '1':
                    mask1.append(35 - i)
                if mask[i] == '0':
                    mask0.append(35 - i)
            continue

        address = int(line.split('[')[1].split(']')[0])
        value = int(line.split('=')[1].strip())

        for i in range(36):
            if i in mask0:
                if value & (1 << i) != 0:
                    value -= 1 << i
            if i in mask1:
                if value & (1 << i) == 0:
                    value += 1 << i
        res[address] = value

    total = 0
    for key in res:
        total += res[key]
    return total

def second():
    data = get_data()
    res = {}
    mask_x = []
    mask_1 = []
    for line in data:
        if line[0:4] == 'mask':
            mask = line.split(' = ')[1]
            mask_x = []
            mask_1 = []
            for i in range(0, 36):
                if mask[i] == 'X':
                    mask_x.append(35 - i)
                elif mask[i] == '1':
                    mask_1.append(35 - i)
            continue

        address = int(line.split('[')[1].split(']')[0])
        value = int(line.split('=')[1].strip())

        for i in mask_1:
            address = address | (1 << i)

        for i, _ in enumerate(range(2 ** len(mask_x))):
            values = [0] * len(mask_x)
            for j in range(len(mask_x)):
                if i & (1 << j) != 0:
                    values[j] = 1

            for j, x in zip(values, mask_x):
                if j == 0:
                    address = address & ~(1 << x)
                if j == 1:
                    address = address | (1 << x)
            res[address] = value

    total = 0
    for key in res:
        total += res[key]
    return total

print(f"First:  {first()}")
print(f"Second: {second()}")
