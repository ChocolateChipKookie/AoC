#Advent of Code 2018 day 15
from util import *
DAY = 15
YEAR = 2018


class Combat:
    def __init__(self, health=200, goblin_attack=3, elf_attack=3):
        lines = input_lines(DAY, YEAR)
        self.data = [[c for c in line] for line in lines]
        self.width, self.height = len(self.data[0]), len(self.data)
        self.entities = []
        attacks = {"G": goblin_attack, "E": elf_attack}
        for y, line in enumerate(self.data):
            for x, c in enumerate(line):
                if c in "GE":
                    self.entities.append([(x, y), c, health, attacks[c]])
        self.movement = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        self.t = 0

    def reading_order(self, pos):
        return pos[0] + pos[1] * self.width

    def distance(self, start, end):
        if start == end:
            return 0
        to_check = []
        checked = set()
        to_check.append((start, 0))

        while len(to_check) > 0:
            pos, dist = to_check.pop(0)
            if pos in checked:
                continue
            checked.add(pos)
            for m in self.movement:
                npos = pos[0] + m[0], pos[1] + m[1]
                if npos == end:
                    return dist + 1
                if self.is_walkable(npos) and npos not in checked and npos:
                    to_check.append((npos, dist + 1))

        return -1

    def is_walkable(self, pos):
        return self.data[pos[1]][pos[0]] == "."

    def find_enemies(self, entity):
        enemy_squares = set()
        for e in self.entities:
            if e[1] == entity[1]:
                continue
            if e[2] <= 0:
                continue
            for m in self.movement:
                pos = (e[0][0] + m[0], e[0][1] + m[1])
                if self.is_walkable(pos):
                    enemy_squares.add(pos)
        enemy_squares = [(p, self.distance(entity[0], p)) for p in enemy_squares]
        enemy_squares = [p for p in enemy_squares if p[1] > 0]
        return sorted(enemy_squares, key=lambda x: x[1])

    def round(self):
        self.entities.sort(key=lambda e: self.reading_order(e[0]))
        opposite = {
            "E": [e for e in self.entities if e[1] == "G"],
            "G": [e for e in self.entities if e[1] == "E"],
        }

        def count_entitites(entities):
            return sum(1 for e in entities if e[2] > 0)

        def try_attack(entity):
            pos, c, health, attack = entity
            targets = []
            for m in self.movement:
                npos = pos[0] + m[0], pos[1] + m[1]
                nc = self.data[npos[1]][npos[0]]
                if nc in "EG" and nc != c:
                    target = next(e for e in self.entities if e[0] == npos)
                    if target[2] > 0:
                        targets.append(target)
            if len(targets) == 0:
                return False

            target = min(targets, key=lambda t: t[2])
            target[2] -= attack
            if target[2] <= 0:
                self.data[target[0][1]][target[0][0]] = "."
            return True

        def clean_dead():
            self.entities = [e for e in self.entities if e[2] > 0]

        for entity in self.entities:
            pos, c, health, attack = entity
            if health <= 0:
                continue
            if try_attack(entity):
                if count_entitites(opposite[c]) == 0:
                    clean_dead()
                    return False
                continue
            enemies = self.find_enemies(entity)
            if len(enemies) == 0:
                continue

            enemies = [e for e in enemies if e[1] == enemies[0][1]]
            enemies.sort(key=lambda x: self.reading_order(x[0]))
            selected = enemies[0]

            next_pos = []
            for m in self.movement:
                npos = pos[0] + m[0], pos[1] + m[1]
                if self.data[npos[1]][npos[0]] == ".":
                    dist = self.distance(selected[0], npos)
                    if dist >= 0:
                        next_pos.append((npos, dist))

            min_dist = min(p[1] for p in next_pos)
            npos = min((p for p in next_pos if p[1] == min_dist), key=lambda p: self.reading_order(p[0]))[0]
            self.data[pos[1]][pos[0]] = "."
            self.data[npos[1]][npos[0]] = c
            entity[0] = npos
            if try_attack(entity):
                if count_entitites(opposite[c]) == 0:
                    clean_dead()
                    return False
        clean_dead()
        self.t += 1
        return True


    def print(self):
        print(f"Round {self.t}:"
              f"")
        for line in self.data:
            print("".join(line))


combat = Combat()
while combat.round():
    pass

round = combat.t
total_health = sum(e[2] for e in combat.entities)

first = round * total_health
print(f"First:  {first}")

second = None
for attack in range(4, 200):
    combat = Combat(elf_attack=attack)
    total_elves = sum(1 for x in combat.entities if x[1] == 'E')
    obliteration = True
    while combat.round():
        elves = sum(1 for x in combat.entities if x[1] == 'E')
        if elves != total_elves:
            obliteration = False
            break
    if obliteration:
        round = combat.t
        total_health = sum(e[2] for e in combat.entities)
        second = round * total_health
        break

print(f"Second: {second}")
