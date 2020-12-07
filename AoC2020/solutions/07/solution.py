#Advent of Code 2020 day 7
from util import *
DAY = 7


def get_data():
    data = input_lines(DAY)
    data = [x.split(' contain ') for x in data]
    data = [(x[0][:-5].strip(), x[1].split(', ')) for x in data]
    data = {x[0]: [y.split() for y in x[1]] for x in data}
    for key in data:
        instance = data[key]
        if instance[0][0] == 'no':
            data[key] = []
        else:
            data[key] = [(" ".join(i[1:3]), int(i[0])) for i in instance]

    return data


def task1(data):
    can_access = set()
    def recursive(bag, goal):
        children = [c[0] for c in data[bag]]
        res = False
        # If the node contains shiny gold, return true
        if goal in children:
            res = True
        elif any((c in can_access) or recursive(c, goal) for c in children):
            res = True
        if res:
            can_access.add(bag)
        return res
    return sum([recursive(bag, 'shiny gold') for bag in data])


def task2(data):
    def recursive(bag):
        children = data[bag]
        # If it contains no bags, return 1
        res = 0
        for c in children:
            # For every bag it contains, add the number of bags it contains
            res += c[1] * recursive(c[0])

        return res + 1

    return recursive('shiny gold') - 1


data = get_data()
first = task1(data)
second = task2(data)

print(f"First:  {first}")
print(f"Second: {second}")
