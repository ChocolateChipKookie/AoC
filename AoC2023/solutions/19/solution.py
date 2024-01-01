# Advent of Code 2023 day 19
from math import prod
from copy import deepcopy
from util import *

YEAR = 2023
DAY = 19


def get_data():
    def parse_rule(line):
        name, rules = line.split("{")
        rules = rules[:-1].split(",")
        rules = [rule.split(":") for rule in rules]
        return name, rules

    def parse_variables(line):
        variables = line[1:-1].split(",")
        return {n: int(i) for n, i in [v.split("=") for v in variables]}

    lines = iter(input_lines(DAY, YEAR))
    rules = {}
    for line in lines:
        if not line:
            break
        name, rule = parse_rule(line)
        rules[name] = rule

    variables = [parse_variables(l) for l in lines]

    return rules, variables


def check(state, rule_name="in"):
    if rule_name in ["R", "A"]:
        return rule_name == "A"
    current_rules = rules[rule_name]
    for rule in current_rules:
        if len(rule) == 1:
            return check(state, rule[0])
        if eval(rule[0], {}, state):
            return check(state, rule[1])


def split(state, statement):
    var, op, number = statement[0], statement[1], int(statement[2:])
    current = state[var]

    if number >= current[1]:
        return (None, state) if op == ">" else (state, None)

    if current[0] > number:
        return (state, None) if op == ">" else (None, state)

    state, other = deepcopy(state), deepcopy(state)

    if op == ">":
        state[var] = number + 1, current[1]
        other[var] = current[0], number
    else:
        state[var] = current[0], number - 1
        other[var] = number, current[1]
    return state, other


def explore(state, rule_name="in"):
    if rule_name == "R":
        return 0
    if rule_name == "A":
        return prod((ma - mi + 1) for mi, ma in state.values())

    total = 0
    for rule in rules[rule_name]:
        if state is None:
            break
        if len(rule) == 1:
            total += explore(state, rule[0])
            break
        substate, state = split(state, rule[0])
        if substate is not None:
            total += explore(substate, rule[1])
    return total


rules, variables = get_data()

first = sum(sum(v.values()) for v in variables if check(v))
second = explore({k: (1, 4000) for k in "xmas"})

print("First:  ", first)
print("Second: ", second)
