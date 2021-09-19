#Advent of Code 2018 day 2
from util import *
DAY = 2
YEAR = 2018


def get_data():
    return input_lines(DAY, YEAR)


data = get_data()

counter = {x:0 for x in range(len(data[0]))}
for id in data:
    for x in set(id.count(x) for x in set(id)):
        counter[x] += 1

first = counter[2] * counter[3]


def difference(str1, str2):
    diff = []
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diff.append(i)
    return diff


second = None
for id1 in data:
    for id2 in data:
        diff = difference(id1, id2)
        if len(diff) == 1:
            d = diff[0]
            second = id1[:d] + id1[d+1:]

print(f"First:  {first}")
print(f"Second: {second}")
