#Advent of Code 2018 day 14
from util import *
DAY = 14
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()[0]
data_i = int(get_data()[0])
scoreboard = "37"
positions = [0, 1]

while len(scoreboard) < data_i + 10:
    s1, s2 = int(scoreboard[positions[0]]), int(scoreboard[positions[1]])
    scoreboard += str(s1 + s2)
    positions[0] = (positions[0] + 1 + s1) % len(scoreboard)
    positions[1] = (positions[1] + 1 + s2) % len(scoreboard)

first = scoreboard[data_i:data_i+10]

while True:
    s1, s2 = int(scoreboard[positions[0]]), int(scoreboard[positions[1]])
    scoreboard += str(s1 + s2)
    positions[0] = (positions[0] + 1 + s1) % len(scoreboard)
    positions[1] = (positions[1] + 1 + s2) % len(scoreboard)

    if data in scoreboard[-12:]:
        break

second = scoreboard.find(data)

print(f"First:  {first}")
print(f"Second: {second}")
