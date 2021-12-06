#Advent of Code 2018 day 16
from util import *
DAY = 16
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
data_1 = []
data_2 = None
for i in range(0, len(data), 4):
    values = data[i:i+3]
    if values[0] != "":
        r0 = tuple(int(x) for x in values[0][9:-1].split(", "))
        op = tuple(int(x) for x in values[1].split())
        r1 = tuple(int(x) for x in values[2][9:-1].split(", "))
        data_1.append((op, r0, r1))
    else:
        data_2 = [x.split() for x in data[i:] if x != ""]
        data_2 = [tuple(int(y) for y in x) for x in data_2]
        break


def alu(dest, reg, op):
    reg[dest] = op(reg)

operations = {}
operations["addr"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] + r[val[1]])
operations["addi"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] + val[1])
operations["mulr"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] * r[val[1]])
operations["muli"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] * val[1])
operations["borr"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] | r[val[1]])
operations["bori"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] | val[1])
operations["banr"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] & r[val[1]])
operations["bani"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]] & val[1])
operations["setr"] = lambda val, reg: alu(val[2], reg, lambda r: r[val[0]])
operations["seti"] = lambda val, reg: alu(val[2], reg, lambda r: val[0])
operations["gtir"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if val[0] > r[val[1]] else 0)
operations["gtri"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if r[val[0]] > val[1] else 0)
operations["gtrr"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if r[val[0]] > r[val[1]] else 0)
operations["eqir"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if val[0] == r[val[1]] else 0)
operations["eqri"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if r[val[0]] == val[1] else 0)
operations["eqrr"] = lambda val, reg: alu(val[2], reg, lambda r: 1 if r[val[0]] == r[val[1]] else 0)

def plausible_operations(opcode, input, output):
    count = 0
    output = tuple(output)
    for op in operations:
        reg = [x for x in input]
        operations[op](opcode[1:], reg)
        if tuple(reg) == output:
            count += 1
    return count

first = sum(1 for x in data_1 if plausible_operations(*x) >= 3)

codes = {}
unresolved = set(x for x in operations)

while len(unresolved) > 0:
    plausible = {x: set() for x in range(len(operations))}
    for opcode, r_in, r_out in data_1:
        output = tuple(r_out)
        for op in unresolved:
            code = opcode[0]
            reg = [x for x in r_in]
            operations[op](opcode[1:], reg)
            if tuple(reg) == output:
                plausible[code].add(op)

    resolving = None
    for code in plausible:
        if len(plausible[code]) == 1:
            resolving = (code, next(iter(plausible[code])))

    unresolved.remove(resolving[1])
    codes[resolving[0]] = resolving[1]
    data_1 = [x for x in data_1 if x[0][0] != resolving[0]]

reg = [0, 0, 0, 0]
for opcode in data_2:
    code = codes[opcode[0]]
    operations[code](opcode[1:], reg)

second = reg[0]

print(f"First:  {first}")
print(f"Second: {second}")
