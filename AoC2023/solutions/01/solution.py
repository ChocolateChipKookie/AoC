# Advent of Code 2023 day 1
from util import *

YEAR = 2023
DAY = 1


def get_data():
    return input_lines(DAY, YEAR)


def get_number(val):
    digits = [c for c in val if c.isdigit()]
    return int(digits[0] + digits[-1])


def get_written_number(val):
    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for i in range(10):
        numbers[str(i)] = i

    digits = []
    current_index = 0
    while current_index < len(val):
        ss = val[current_index:]
        for n, v in numbers.items():
            if len(ss) < len(n):
                continue
            if ss[: len(n)] == n:
                digits.append(v)
                break
        current_index += 1

    result = digits[0] * 10 + digits[-1]
    return result


data = get_data()

first = sum(get_number(x) for x in data)
second = sum(get_written_number(x) for x in data)

print("First:  ", first)
print("Second: ", second)
