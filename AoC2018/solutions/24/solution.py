#Advent of Code 2018 day 24
from util import *
import copy
YEAR = 2018
DAY = 24


class Group:
    def __init__(self, description: str):
        numbers = re.findall(r'\d+', description)
        self.units      = int(numbers[0])
        self.hit_points = int(numbers[1])
        self.attack     = int(numbers[2])
        self.initiative = int(numbers[3])
        self.immune = set()
        self.weak = set()

        self.attack_type = description.split()[-5]

        if "(" in description:
            details_start = description.find("(") + 1
            details_end = description.find(")")
            details = description[details_start:details_end].split(';')
            for detail in details:
                tokens = detail.split()
                values = (token.strip(',') for token in tokens[2:])
                if tokens[0] == "immune":
                    self.immune.update(values)
                else:
                    self.weak.update(values)

    def effective_power(self) -> int:
        return self.units * self.attack

    def dead(self) -> bool:
        return self.units == 0

    def calculate_damage(self, other: 'Group') -> int:
        if self.attack_type in other.immune:
            return 0
        if self.attack_type in other.weak:
            return self.effective_power() * 2
        return self.effective_power()

    def attack_other(self, other: 'Group') -> None:
        damage: int = self.calculate_damage(other)
        units_lost = damage // other.hit_points
        other.units = max(0, other.units - units_lost)


def get_data():
    groups = []
    for line in input_lines(DAY, YEAR):
        if not line:
            continue
        if len(line.split()) <= 2:
            groups.append([])
            continue
        groups[-1].append(Group(line))

    return groups


def choose_opponents(attackers: list, defenders: list) -> dict:
    available_picks = set(defenders)
    picks = {}

    def comp_key(group: Group):
        return group.effective_power() * 1000 + group.initiative

    attackers.sort(key=comp_key, reverse=True)
    for attacker in attackers:
        if not available_picks:
            break
        potentials = list(available_picks)
        potentials = sorted(potentials, key=lambda x: attacker.calculate_damage(x), reverse=True)
        max_val = attacker.calculate_damage(potentials[0])
        if max_val == 0:
            continue
        potentials = list(filter(lambda x: attacker.calculate_damage(x) == max_val, potentials))
        potentials.sort(key=comp_key, reverse=True)
        picks[attacker] = potentials[0]
        available_picks.remove(potentials[0])

    return picks


def fight(immune, infection, boost=0):
    for group in immune:
        group.attack += boost
    iteration = 0
    while immune and infection:
        iteration += 1
        if iteration > 5000:
            break
        all_picks = {}
        all_picks.update(choose_opponents(immune, infection))
        all_picks.update(choose_opponents(infection, immune))
        all_groups = immune + infection
        all_groups.sort(key=lambda x: x.initiative, reverse=True)

        for attacker in all_groups:
            if attacker in all_picks:
                defender = all_picks[attacker]
                attacker.attack_other(defender)

        for group in all_groups:
            if group.units != 0:
                continue
            if group in immune:
                immune.remove(group)
            if group in infection:
                infection.remove(group)


immune, infection = get_data()
fight(immune, infection)
first = sum(x.units for x in (immune + infection))


immune, infection = get_data()
lo, hi, mid = 0, 1000, 0

while lo < hi:
    mid = (lo + hi) // 2
    imm, inf = copy.deepcopy(immune), copy.deepcopy(infection)
    fight(imm, inf, mid)
    success = len(inf) == 0
    if success:
        hi = mid
    else:
        lo = mid + 1

imm, inf = copy.deepcopy(immune), copy.deepcopy(infection)
fight(imm, inf, lo)
second = sum(x.units for x in imm)

print("First:  ", first)
print("Second: ", second)
