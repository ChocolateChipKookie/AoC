# Advent of Code 2023 day 7
from util import *
from collections import Counter
from functools import cmp_to_key

YEAR = 2023
DAY = 7

HandBid = tuple[str, int]


def get_data() -> list[tuple[str, int]]:
    tokens = (t.split() for t in input_lines(DAY, YEAR))
    return [(h, int(n)) for h, n in tokens]


def compare(h1: HandBid, h2: HandBid, joker_rule: bool = False):
    def get_type(h: str) -> int:
        counts = dict(Counter(h))
        if joker_rule:
            counts.pop("J", 0)
            if not counts:
                # For the edge case that the hand is only J
                return 6
            opt = max(counts, key=lambda k: counts[k])
            counts = dict(Counter(h.replace("J", opt)))
        if len(counts) == 1:
            # Five of a kind
            return 6
        if len(counts) == 2:
            # Four of a kind or full house
            return 5 if max(counts.values()) == 4 else 4
        if len(counts) == 3:
            # Three of a kind or 2 pairs
            return 3 if max(counts.values()) == 3 else 2
        if len(counts) == 4:
            # One pair
            return 1
        # Nothing
        return 0

    def to_vals(h: str):
        strengths = "AKQJT98765432"
        if joker_rule:
            strengths = "AKQT98765432J"
        return [len(strengths) - strengths.index(v) for v in h]

    t1 = get_type(h1[0])
    t2 = get_type(h2[0])

    if t1 == t2:
        return -1 if to_vals(h1[0]) < to_vals(h2[0]) else 1
    return -1 if t1 < t2 else 1


def compare_joker(h1, h2):
    return compare(h1, h2, True)


def calc_winnings(sorted_data):
    return sum(i * val[1] for i, val in enumerate(sorted_data, 1))


data = get_data()

sorted_data = sorted(data, key=cmp_to_key(compare))
first = calc_winnings(sorted_data)
sorted_data_jokers = sorted(data, key=cmp_to_key(compare_joker))
second = calc_winnings(sorted_data_jokers)

print("First:  ", first)
print("Second: ", second)
