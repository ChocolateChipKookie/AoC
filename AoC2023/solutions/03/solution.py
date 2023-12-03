#Advent of Code 2023 day 3
from util import *
from dataclasses import dataclass, field
YEAR = 2023
DAY = 3

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
grid = [[c for c in s] for s in data]

@dataclass
class Number:
    n: int = 0
    adjacent: set[tuple[int, int]] = field(default_factory=set)

    def is_adjacent(self, part: tuple[int, tuple[int, int]]):
        def max_manhattan(p1, p2):
            dx = abs(p1[0] - p2[0])
            dy = abs(p1[1] - p2[1])
            return max(dx, dy)
        return any(max_manhattan(part[1], p) <= 1 for p in self.adjacent)

numbers: list[Number]= []
parts = []

for j, line in enumerate(grid):
    current_number = None
    for i,  val in enumerate(line):
        if val.isdigit():
            if not current_number:
                current_number = Number()
            current_number.n *= 10
            current_number.n += int(val)
            current_number.adjacent.add((i, j))
        else:
            if current_number:
                numbers.append(current_number)
                current_number = None
            if val != ".":
                parts.append((val, (i, j)))
    if current_number:
        numbers.append(current_number)


first = 0
for n in numbers:
    for p in parts:
        if n.is_adjacent(p):
            first += n.n
            break

second = 0
for p in [part for part in parts if part[0] == "*"]:
    adjacent_numbers = [n.n for n in numbers if n.is_adjacent(p)]
    if len(adjacent_numbers) == 2:
        second += adjacent_numbers[0] * adjacent_numbers[1]

print("First:  ", first)
print("Second: ", second)
