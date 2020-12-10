#Advent of Code 2020 day 10
from util import *
DAY = 10


def get_data():
    return input_integers(DAY)


# Sort data in beforehand
data = sorted(get_data())
joltage = 0
skips = {x:0 for x in range(1, 4)}

# While there is next, select it
while True:
    try:
        selected = next(filter(lambda x: x in range(joltage + 1, joltage+4), data))
        skips[selected - joltage] += 1
        joltage = selected
    except:
        break

# Result joltage and result
joltage += 3
first = skips[1] * (skips[3] + 1)

# So the recursion works
data.append(0)
ways = {0:1}

# Recursive dyamic function that
def recursion(joltage):
    res = 0
    for x in filter(lambda x: x in range(joltage-3, joltage), data):
        if x not in ways:
            ways[x] = recursion(x)
        res += ways[x]
    return res

# second solution
second = recursion(joltage)

print(f"First:  {first}")
print(f"Second: {second}")
