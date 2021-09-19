#Advent of Code 2018 day 12
from util import *
DAY = 12
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)


data = get_data()

initial_state = data[0].split()[2]
initial_state = {x: initial_state[x] for x in range(len(initial_state))}
state = initial_state
rules = [x.split() for x in data[2:]]
rules = {x[0]: x[2] for x in rules}

def calc_score(current):
    score = 0
    for x in current:
        if current[x] == '#':
            score += x
    return score

def step(current):
    min_ = None
    max_ = None
    next_step = {}
    for x in current:
        if current[x] == '#':
            if min_ is None:
                min_ = max_ = x
            else:
                min_ = min(min_, x)
                max_ = max(max_, x)
    for i in range(min_ - 2, max_ + 3):
        r = [current.get(i + x, ".") for x in range(-2, 3)]
        r = "".join(r)
        n = rules[r]
        next_step[i] = n
    return  next_step


def to_string(current):
    min_ = None
    max_ = None
    for x in current:
        if current[x] == '#':
            if min_ is None:
                min_ = max_ = x
            else:
                min_ = min(min_, x)
                max_ = max(max_, x)
    return "".join(current[i] for i in range(min_, max_ + 1))


for i in range(20):
    state = step(state)
first = calc_score(state)

state = initial_state
t = 0
existed = {to_string(state): (calc_score(state), t)}
while True:
    state = step(state)
    state_str = to_string(state)
    t += 1
    if state_str in existed:
        break
    else:
        existed[state_str] = (calc_score(state), t)

score, time = existed[state_str]
score_diff = calc_score(state) - score
period = t - time
# For my input the period was 1 so this works, if the period is not 1 more maths is needed
generations = 50000000000
second = (generations - time) * score_diff + score

print(f"First:  {first}")
print(f"Second: {second}")
