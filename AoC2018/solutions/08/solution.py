#Advent of Code 2018 day 8
from util import *
DAY = 8
YEAR = 2018

def get_data():
    return [int(x) for x in input_tokens(DAY, YEAR)]

data = get_data()

class Tree:
    class Node:
        def __init__(self, children, metadata):
            self.children = children
            self.metadata = metadata

    def __init__(self, data):
        self.data = list(data)
        _, self.root = self.parse(data)

    def parse(self, data):
        n_children, n_metadata = data[:2]
        data = data[2:]
        if n_children == 0:
            metadata = data[:n_metadata]
            data = data[n_metadata:]
            return data, self.Node([], metadata)

        children = []
        for i in range(n_children):
            data, child = self.parse(data)
            children.append(child)

        metadata = data[:n_metadata]
        data = data[n_metadata:]
        return data, self.Node(children, metadata)


def tree_sum(node):
    total = sum(node.metadata)
    for child in node.children:
        total += tree_sum(child)
    return total


def tree_value(node):
    if len(node.children) == 0:
        return sum(node.metadata)
    total = 0
    values = [tree_value(child) for child in node.children]
    for i in node.metadata:
        i -= 1
        if i < 0 or i >= len(node.children):
            continue
        total += values[i]

    return total


tree = Tree(data)
first = tree_sum(tree.root)
second = tree_value(tree.root)

print(f"First:  {first}")
print(f"Second: {second}")
