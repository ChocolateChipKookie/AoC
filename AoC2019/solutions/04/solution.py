#Advent of Code 2019 day 4
from util import *
DAY = 4
YEAR = 2019

def get_data():
    return input_integers(DAY, YEAR)

min_, max_ = get_data()

first = len([1 for x in range(min_, max_) if len(set(str(x))) < 6 and str(x) == "".join(sorted(str(x)))])
second = len([1 for x in range(min_, max_) if 2 in {i: str(x).count(i) for i in set(str(x))}.values() and str(x) == "".join(sorted(str(x)))])

print(f"First:  {first}")
print(f"Second: {second}")
