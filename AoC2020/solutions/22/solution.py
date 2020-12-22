#Advent of Code 2020 day 22
from util import *
DAY = 22
import copy

def get_data():
    cards = [[], []]
    i = 0
    for line in input_lines(DAY):
        if line == "":
            i += 1
        if line.isnumeric():
            cards[i].append(int(line))
    return cards

data = get_data()

def first(data):
    cards = copy.deepcopy(data)
    while True:
        if len(cards[0]) == 0:
            winner = 1
            break
        if len(cards[1]) == 0:
            winner = 0
            break
        round = []
        round.append(cards[0].pop(0))
        round.append(cards[1].pop(0))
        winner = 0
        if round[1] > round[0]:
            winner = 1

        if winner == 1:
            round = list(reversed(round))
        cards[winner].extend(round)

    result = 0
    for i, value in enumerate(cards[winner][::-1]):
        result += (i+1) * value
    return result

def second(data):
    def game(cards, depth):
        seen_configurations = set()
        while True:
            if str(cards) in seen_configurations:
                return 0
            seen_configurations.add(str(cards))

            if len(cards[0]) == 0:
                return 1
            if len(cards[1]) == 0:
                return 0

            round = []
            round.append(cards[0].pop(0))
            round.append(cards[1].pop(0))

            if (len(cards[0]) >= round[0]) and (len(cards[1]) >= round[1]):
                decks = [cards[0][0:round[0]], cards[1][0:round[1]]]
                winner = game(copy.deepcopy(decks), depth + 1)
            else:
                winner = 0
                if round[1] > round[0]:
                    winner = 1

            if winner == 1:
                round = list(reversed(round))
            cards[winner].extend(round)


    data = copy.deepcopy(data)
    winner = game(data, 0)

    result = 0
    for i, value in enumerate(data[winner][::-1]):
        result += (i+1) * value
    return result


print(f"First:  {first(data)}")
print(f"Second: {second(data)}")
