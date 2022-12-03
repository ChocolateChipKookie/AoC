#Advent of Code 2022 day 2
from util import *
YEAR = 2022
DAY = 2


def get_data():
    return input_lines(DAY, YEAR)


data = get_data()
pairs = [tuple(s.split()) for s in data]


def first():
    play_scores = {"X": 1, "Y": 2, "Z": 3}
    winning_plays = {"A": "Y", "B": "Z", "C": "X"}
    drawing_plays = {"A": "X", "B": "Y", "C": "Z"}

    total_score = 0
    for p1, p2 in pairs:
        result = 0
        if drawing_plays[p1] == p2:
            result = 3
        elif winning_plays[p1] == p2:
            result = 6
        total_score += result + play_scores[p2]
    return total_score


def second():
    play_map = {
        "A": {"X": 3, "Y": 1, "Z": 2},
        "B": {"X": 1, "Y": 2, "Z": 3},
        "C": {"X": 2, "Y": 3, "Z": 1},
    }

    result_map = {"X": 0, "Y": 3, "Z": 6}

    return sum(play_map[p1][p2] + result_map[p2] for (p1, p2) in pairs)


print("First:  ", first())
print("Second: ", second())
