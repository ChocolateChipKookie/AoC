#Advent of Code 2020 day 7
from util import *
DAY = 7
YEAR = 2020

def get_data():
    data = input_lines(DAY, YEAR)
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

    # Recursively check if goal bag is in given bag type
    def recursive(bag, goal):
        children = [c[0] for c in data[bag]]
        # If goal is in children or (any of the children(already evaluated as can_access or recursive==True))
        res = (goal in children) or any(c in can_access or recursive(c, goal) for c in children)
        if res:
            can_access.add(bag)
        return res

    return sum([recursive(bag, 'shiny gold') for bag in data])

    """
    # Also valid, but recursive() is faster because it stores intermediate results
    def recursive_short(bag, goal):
        children = [c[0] for c in data[bag]]
        return (goal in children) or any(recursive(c, goal) for c in children)

    return sum([recursive_short(bag, 'shiny gold') for bag in data])
    """

def task2(data):
    def recursive(bag):
        children = data[bag]
        # Sum of all children + 1 for this bag
        return sum([c[1] * recursive(c[0]) for c in children]) + 1

    return recursive('shiny gold') - 1


data = get_data()
first = task1(data)
second = task2(data)

print(f"First:  {first}")
print(f"Second: {second}")
