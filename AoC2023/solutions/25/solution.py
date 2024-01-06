# Advent of Code 2023 day 25
from codecs import readbuffer_encode
from util import *

YEAR = 2023
DAY = 25


def get_data():
    connections: dict[str, set[str]] = {}

    def add(l, r):
        if l not in connections:
            connections[l] = set()
        connections[l].add(r)

    for line in input_lines(DAY, YEAR):
        l, r = line.split(": ")
        rc = r.split()
        for c in rc:
            add(l, c)
            add(c, l)
    return connections


data = get_data()
tight_nodes = [(k, v) for k, v in data.items() if len(v) <= 4]

# Group up nodes that have only 4 neighbours
# Logic: A node has to have at least 5 neighbours to be a bridge
groups = []
while tight_nodes:
    group = {tight_nodes.pop(0)[0]}
    while True:
        added = None
        for current in tight_nodes:
            k, v = current
            if not group.isdisjoint(v):
                group.add(k)
                added = current
                break
        if added is None:
            break
        tight_nodes.remove(added)
    groups.append(group)

groups.extend({k} for k, v in data.items() if len(v) > 4)
groups.sort(key=len, reverse=True)

# The 2 largest groups are the main groups
main_groups = groups[:2]
to_merge = groups[2:]
while to_merge:
    current = to_merge.pop(0)
    neighbours = set()
    for val in current:
        neighbours.update(data[val])
    # The parent group is the group that has strictly more of the neighbours in it
    # In the case they are tied, try again later
    lens = [len(l.intersection(neighbours)) for l in main_groups]
    if all(l == lens[0] for l in lens):
        to_merge.append(current)
        continue

    parent = max(main_groups, key=lambda l: len(l.intersection(neighbours)))
    parent.update(current)

first = len(main_groups[0]) * len(main_groups[1])
second = "Free moneys"

print("First:  ", first)
print("Second: ", second)
