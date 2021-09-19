#Advent of Code 2018 day 4
from util import *
DAY = 4
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)


data = sorted(get_data())

shifts = []
current = None
for entry in data:
    tokens = entry.split()
    if "begins" in entry:
        if current:
            if current[1] >= 0:
                current[2].append((current[1], 60))
            shifts.append((current[0], current[2]))
        id = int(tokens[3][1:])
        current = [id, 0, []]
        continue
    timestamp = int(tokens[1][3:5])
    if "falls" in entry:
        current[1] = timestamp
        continue
    if "wakes" in entry:
        current[2].append((current[1], timestamp))
        current[1] = -1
        continue

asleep_for = dict()
for id, asleep in shifts:
    if id not in asleep_for:
        asleep_for[id] = 0
    for timespan in asleep:
        asleep_for[id] += timespan[1] - timespan[0]

guard = max(asleep_for, key=lambda x: asleep_for[x])
asleep = {x: 0 for x in range(60)}
for id, timespans in shifts:
    if guard != id:
        continue
    for timespan in timespans:
        for x in range(timespan[0], timespan[1]):
            asleep[x] += 1

minute = max(asleep, key=lambda x: asleep[x])

first = guard * minute

guards = dict()
for guard in asleep_for:
    asleep = {x: 0 for x in range(60)}
    for id, timespans in shifts:
        if guard != id:
            continue
        for timespan in timespans:
            for x in range(timespan[0], timespan[1]):
                asleep[x] += 1
    minute = max(asleep, key=lambda x: asleep[x])
    length = asleep[minute]
    guards[guard] = (minute, length)

guard = max(guards, key=lambda x: guards[x][1])
minute = guards[guard][0]

second = guard * minute

print(f"First:  {first}")
print(f"Second: {second}")
