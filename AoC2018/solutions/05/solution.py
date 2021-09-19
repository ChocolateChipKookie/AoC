#Advent of Code 2018 day 5
from util import *
import re

DAY = 5
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)


data = get_data()
molecule = data[0]

def collapse(molecule):
    changed = True
    while changed:
        changed = False
        i = 0
        while True:
            if i >= len(molecule) - 1:
                break
            c1, c2 = molecule[i:i+2]
            if c1.lower() == c2.lower() and c1 != c2:
                molecule = molecule[:i] + molecule[i+2:]
                changed = True
            else:
                i += 1
    return molecule

molecule = collapse(molecule)
first = len(molecule)

units = set(x.lower() for x in molecule)
second = len(molecule)

for unit in units:
    modified_molecule = molecule.replace(unit, "").replace(unit.upper(), "")
    modified_molecule = collapse(modified_molecule)
    length = len(modified_molecule)
    if length < second:
        second = length

print(f"First:  {first}")
print(f"Second: {second}")
