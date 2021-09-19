#Advent of Code 2018 day 13
from util import *
import copy
DAY = 13
YEAR = 2018

def get_data():
    return get_input(DAY, YEAR).split('\n')

data = get_data()
data = [[x for x in line] for line in data]

class Simulation:
    def __init__(self, state):
        self.state = state
        self.tracks = state
        self.carts = []
        self.replace = {
            "<": "-",
            ">": "-",
            "^": "|",
            "v": "|"
        }
        self.movement = {
            "<": (-1,  0),
            ">": ( 1,  0),
            "^": ( 0, -1),
            "v": ( 0,  1)
        }

        self.next_direction = {
            ("/", "<"): "v",
            ("/", ">"): "^",
            ("/", "^"): ">",
            ("/", "v"): "<",
            ("\\", "<"): "^",
            ("\\", ">"): "v",
            ("\\", "^"): "<",
            ("\\", "v"): ">",
        }

        self.crossing = {
            ("L", ">"): ("C", "^"),
            ("C", ">"): ("R", ">"),
            ("R", ">"): ("L", "v"),

            ("L", "<"): ("C", "v"),
            ("C", "<"): ("R", "<"),
            ("R", "<"): ("L", "^"),

            ("L", "^"): ("C", "<"),
            ("C", "^"): ("R", "^"),
            ("R", "^"): ("L", ">"),

            ("L", "v"): ("C", ">"),
            ("C", "v"): ("R", "v"),
            ("R", "v"): ("L", "<"),
        }

        for y, line in enumerate(self.state):
            for x, val in enumerate(line):
                if val in "<>v^":
                    self.tracks[y][x] = self.replace[val]
                    self.carts.append([(x, y), "L", val, True])

        self.t = 0
        self.width, self.height = len(state[0]), len(state)
        self.crashes = []

    def tick(self):
        # Sort carts
        self.carts = sorted(self.carts, key=lambda c: c[0][0] + c[0][1] * self.width)
        self.t += 1
        for i, cart in enumerate(self.carts):
            pos, t, direction, active = cart
            if not active:
                continue
            movement = self.movement[direction]
            pos = (pos[0] + movement[0], pos[1] + movement[1])
            cart[0] = pos
            track = self.tracks[pos[1]][pos[0]]
            if track in "/\\":
                cart[2] = self.next_direction[(track, direction)]
            elif track == "+":
                t, direction = self.crossing[(t, direction)]
                cart[1] = t
                cart[2] = direction
            on_position = [c for c in self.carts if c[0] == pos and c[3]]
            if len(on_position) == 2:
                for c in on_position:
                    c[3] = False
                self.crashes.append(pos)

        self.carts = [cart for cart in self.carts if cart[3]]


simulation = Simulation(data)
while len(simulation.carts) > 1:
    simulation.tick()

first = simulation.crashes[0]
second = simulation.carts[0][0]

print(f"First:  {first}")
print(f"Second: {second}")
