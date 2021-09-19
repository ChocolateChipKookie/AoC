#Advent of Code 2020 day 18
from util import *
DAY = 18
YEAR = 2020


def get_data():
    return input_lines(DAY, YEAR)


data = get_data()


def parse(str):
    str = str.replace("(", " ( ").replace(")", " ) ")
    return str.split()


def first(data):
    def evaluate(tokens):
        if len(tokens) == 1:
            return int(tokens[0])

        def create_tree(tokens):
            res = []
            i = 0
            while i < len(tokens):
                if tokens[i].isnumeric():
                    res.append([tokens[i]])
                    i += 1
                    continue

                if tokens[i] in "*+":
                    res.append(tokens[i])
                    i += 1
                    continue

                if tokens[i] == '(':
                    depth = 1
                    i += 1
                    begin = i
                    while True:
                        if tokens[i] == '(':
                            depth += 1
                        if tokens[i] == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        i += 1
                    end = i
                    res.append(tokens[begin:end])
                    i += 1

            return res

        tree = create_tree(tokens)

        current = evaluate(tree[0])
        i = 1
        while i < len(tree):
            if tree[i] == '*':
                current *= evaluate(tree[i+1])
            if tree[i] == '+':
                current += evaluate(tree[i+1])
            i += 2
        return current

    return sum(evaluate(parse(line)) for line in data)


def second(data):
    def evaluate(tokens):
        if len(tokens) == 1:
            return int(tokens[0])

        def create_tree(tokens):
            res = []
            i = 0
            while i < len(tokens):
                if tokens[i].isnumeric():
                    res.append([tokens[i]])
                    i += 1
                    continue

                if tokens[i] in "*+":
                    res.append(tokens[i])
                    i += 1
                    continue

                if tokens[i] == '(':
                    depth = 1
                    i += 1
                    begin = i
                    while True:
                        if tokens[i] == '(':
                            depth += 1
                        if tokens[i] == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        i += 1
                    end = i
                    res.append(tokens[begin:end])
                    i += 1

            return res

        tree = create_tree(tokens)

        for i in range(0, len(tree), 2):
            tree[i] = evaluate(tree[i])

        while '+' in tree:
            index = tree.index('+')
            tree[index - 1: index+2] = [tree[index-1] + tree[index+1]]

        while '*' in tree:
            index = tree.index('*')
            tree[index - 1: index+2] = [tree[index-1] * tree[index+1]]
        return tree[0]

    return sum(evaluate(parse(line)) for line in data)

print(f"First:  {first(data)}")
print(f"Second: {second(data)}")
