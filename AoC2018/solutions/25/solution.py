#Advent of Code 2018 day 25
import random

from util import *
YEAR = 2018
DAY = 25


def get_data():
    return [tuple(int(x) for x in line.split(',')) for line in input_lines(DAY, YEAR)]


class Constellation:
    def __init__(self, point):
        self.original = point
        self.points = [point]
        self.min = [x - 3 for x in point]
        self.max = [x + 3 for x in point]

    @staticmethod
    def distance(p1, p2):
        return sum(abs(x1 - x2) for x1, x2 in zip(p1, p2))

    def close(self, point):
        for i in range(4):
            if not (self.min[i] <= point[i] <= self.max[i]):
                return False
        return True

    def update_minmax(self, point):
        for i in range(4):
            self.min[i] = min(point[i] - 3, self.min[i])
            self.max[i] = max(point[i] + 3, self.max[i])

    def collides(self, point):
        if self.close(point):
            for p in self.points:
                if self.distance(p, point) <= 3:
                    return True
        return False

    def try_add(self, other: 'Constellation'):
        other.points.sort(key=lambda x: self.distance(self.original, x))

        for point in other.points:
            if self.collides(point):
                self.points.extend(other.points)
                for i in range(4):
                    self.min[i] = min(other.min[i], self.min[i])
                    self.max[i] = max(other.max[i], self.max[i])
                return True
        return False


finished = []
constellations = [Constellation(point) for point in get_data()]

while constellations:
    constellations.sort(key=lambda c: len(c.points))
    constellation = constellations.pop(0)

    success = False
    for other in constellations:
        if constellation.try_add(other):
            constellations.remove(other)
            constellations.append(constellation)
            success = True
            break

    if not success:
        finished.append(constellation)


first = len(finished)
second = "Free moneys"

print("First:  ", first)
print("Second: ", second)