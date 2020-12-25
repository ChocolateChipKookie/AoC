#Advent of Code 2020 day 25
from util import *
DAY = 25

def get_data():
    return input_lines(DAY)

data = get_data()

card_pubkey = int(data[0])
door_pubkey = int(data[1])

card_loop = 0
door_loop = 0

mod = 20201227
subject = 7
current = 1
i = 0

while True:
    current *= subject
    current = current % mod
    i +=1
    if current == card_pubkey:
        card_loop = i
    if current == door_pubkey:
        door_loop = i

    if card_loop != 0 and door_loop != 0:
        break

first = 1
subject = card_pubkey
for i in range(door_loop):
    first *= subject
    first = first % mod


second = "Free money!"

print(f"First:  {first}")
print(f"Second: {second}")
