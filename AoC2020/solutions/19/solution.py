#Advent of Code 2020 day 19
from util import *
DAY = 19
YEAR = 2020


def get_data():
    return input_lines(DAY, YEAR)


data = get_data()


def full():

    def first(data):
        rules = {}
        samples = []
        add_sample = False
        for line in data:
            if line == "":
                add_sample = True
                continue
            if add_sample:
                samples.append(line)
            else:
                tokens = line.split(':')
                rule = tokens[0]
                rules[rule] = [[y.replace('"', '') for y in x.split()] for x in tokens[1].strip().split("|")]

        def match(rule, str):
            def recursive(rule, str):
                # Fetch the paths for the rule
                paths = rules[rule]
                if paths[0][0] in 'ab':
                    if len(str) == 0:
                        return False, 0
                    if paths[0][0] == str[0]:
                        return True, 1
                    else:
                        return False, 0

                # Check if any path of a rule is valid
                for rule_string in paths:
                    pattern = str
                    total_len = 0
                    is_valid = True
                    # Check if every part of the path is valid
                    for rule in rule_string:
                        valid, length = recursive(rule, pattern)
                        if not valid:
                            is_valid = False
                            break
                        pattern = pattern[length:]
                        total_len += length
                    if is_valid:
                        return True, total_len
                return False, 0

            valid, length = recursive(rule, str)
            return valid and length == len(line)

        count = 0
        for line in samples:
            if match('0', line):
                count += 1

        return count


    def second(data):
        rules = {}
        samples = []
        add_sample = False
        for line in data:
            if line == "":
                add_sample = True
                continue
            if add_sample:
                samples.append(line)
            else:
                tokens = line.split(':')
                rule = tokens[0]
                rules[rule] = [[y.replace('"', '') for y in x.split()] for x in tokens[1].strip().split("|")]

        rules['8'] =  [['42'], ['42', '8']]
        rules['11'] = [['42', '31'], ['42', '11', '31']]

        def unroll(rule):
            possible = rules[rule]
            if possible[0][0] in "ab":
                return possible[0]

            res = []
            for ruleset in possible:
                tmp = [""]
                for r in ruleset:
                    unrolled = unroll(r)
                    tmptmp = []
                    for s1 in tmp:
                        for s2 in unrolled:
                            tmptmp.append(s1+s2)
                    tmp = tmptmp
                for v in tmp:
                    res.append(v)
            return res

        u42 = set(unroll('42'))
        u31 = set(unroll('31'))

        len_token = len(next(iter(u42)))

        def match(line):
            if len(line) % len_token != 0:
                return False
            tokens = [line[x:x+len_token] for x in range(0, len(line), len_token)]
            mapping = []
            for token in tokens:
                if token in u42:
                    mapping.append(0)
                elif token in u31:
                    mapping.append(1)
                else:
                    mapping.append(2)
            if 2 in mapping:
                return False
            if mapping != sorted(mapping):
                return False

            zeros = sum(1 for x in mapping if x == 0)
            ones  = sum(1 for x in mapping if x == 1)
            return zeros > ones > 0

        count = sum(1 for line in samples if match(line))
        return count

    print(f"First:  {first(data)}")
    print(f"Second: {second(data)}")


def simple():
    rules = {}
    samples = []
    add_sample = False
    for line in data:
        if line == "":
            add_sample = True
            continue
        if add_sample:
            samples.append(line)
        else:
            tokens = line.split(':')
            rule = tokens[0]
            rules[rule] = [[y.replace('"', '') for y in x.split()] for x in tokens[1].strip().split("|")]

    def unroll(rule):
        possible = rules[rule]
        if possible[0][0] in "ab":
            return possible[0]

        res = []
        for ruleset in possible:
            tmp = [""]
            for r in ruleset:
                unrolled = unroll(r)
                tmptmp = []
                for s1 in tmp:
                    for s2 in unrolled:
                        tmptmp.append(s1+s2)
                tmp = tmptmp
            for v in tmp:
                res.append(v)
        return res

    u0 = unroll('0')
    first = sum(1 for line in samples if line in u0)

    u42 = set(unroll('42'))
    u31 = set(unroll('31'))
    len_token = len(next(iter(u42)))

    def match(line):
        if len(line) % len_token != 0:
            return False
        tokens = [line[x:x+len_token] for x in range(0, len(line), len_token)]
        mapping = []
        for token in tokens:
            if token in u42:
                mapping.append(0)
            elif token in u31:
                mapping.append(1)
            else:
                mapping.append(2)
        if 2 in mapping:
            return False
        if mapping != sorted(mapping):
            return False

        zeros = sum(1 for x in mapping if x == 0)
        ones  = sum(1 for x in mapping if x == 1)
        return zeros > ones > 0

    second = sum(1 for line in samples if match(line))

    print(f"First:  {first}")
    print(f"Second: {second}")

simple()



