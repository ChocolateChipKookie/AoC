#Advent of Code 2020 day 16
from util import *
import math
DAY = 16

def get_data():
    return get_input(DAY)

data = get_data()
tokens = data.split('\n\n')
rules = [ get_integers(x) for x in tokens[0].split('\n')]

my = get_integers(tokens[1].split('\n')[1])
other = [get_integers(x) for x in tokens[2].split('\n')[1:]]

def first():
    local_rules = []
    for rule in rules:
        local_rules.append((rule[0], rule[1]))
        local_rules.append((rule[2], rule[3]))

    def in_any(number):
        all = [ number in range(x[0], x[1]+1) for x in local_rules]
        return any(all)

    total = 0
    for ticket in other:
        for number in ticket:
            if not in_any(number):
                total += number

    return total

def second():
    local_rules = []
    for rule in rules:
        local_rules.append((rule[0], rule[1]))
        local_rules.append((rule[2], rule[3]))

    def in_any_rule(number):
        all = [ number in range(x[0], x[1]+1) for x in local_rules]
        return any(all)

    invalid = []
    for i in range(len(other)):
        if any([not in_any_rule(number) for number in other[i]]):
            invalid.append(i)

    invalid = sorted(invalid, reverse=True)
    for x in invalid:
        del other[x]

    # Each list in this list lists possible positions for rule
    possible_rules = []

    for position in range(len(rules)):
        possible_rules.append([])
        for i, rule in enumerate(rules):
            valid = True

            for ticket in other:
                value = ticket[position]
                if not (value in range(rule[0], rule[1]+1) or value in range(rule[2], rule[3]+1)):
                    valid = False
            if valid:
                possible_rules[-1].append(i)

    reduced = set()
    while True:
        # exit
        if all([len(x) == 1 for x in possible_rules]):
            break

        reduce = 0
        for i in range(len(rules)):
            if len(possible_rules[i]) == 1:
                reduce = possible_rules[i][0]
                if reduce not in reduced:
                    break

        reduced.add(reduce)
        for i in range(len(rules)):
            if len(possible_rules[i]) > 1:
                if reduce in possible_rules[i]:
                    possible_rules[i].remove(reduce)

    rules_dict = {x[1][0]: x[0] for x in enumerate(possible_rules)}

    departure = [my[rules_dict[x]] for x in range(6)]
    return math.prod(departure)


print(f"First:  {first()}")
print(f"Second: {second()}")
