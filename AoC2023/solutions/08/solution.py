# Advent of Code 2023 day 8
from dataclasses import dataclass
import math
from util import *

YEAR = 2023
DAY = 8


def get_data() -> tuple[str, dict[str, list[str]]]:
    lines = input_lines(DAY, YEAR)
    instructions = lines[0]
    result: dict[str, list[str]] = {}
    for line in lines[2:]:
        lr = line.split(" = ")
        result[lr[0]] = lr[1][1:-1].split(", ")
    return instructions, result


def count_steps(instrunctions: str, mapping: dict[str, list[str]]):
    total_steps = 0
    current = "AAA"
    while current != "ZZZ":
        right = instrunctions[total_steps % len(instrunctions)] == "R"
        current = mapping[current][int(right)]
        total_steps += 1
    return total_steps


@dataclass
class GhostDescriptor:
    start: str
    current: str
    end: str | None = None
    first_end: int = 0
    loop_size: int = 0


def count_steps_ghostly(
    instrunctions: str, mapping: dict[str, list[str]]
) -> int:
    step = 0
    ghosts = [GhostDescriptor(x, x) for x in mapping if x.endswith("A")]
    all_ghosts = [g for g in ghosts]
    while ghosts:
        index = step % len(instrunctions)
        right = instrunctions[index] == "R"
        step += 1
        for ghost in ghosts:
            ghost.current = mapping[ghost.current][int(right)]
            if ghost.current.endswith("Z"):
                ghost.end = ghost.current
                if not ghost.first_end:
                    ghost.first_end = step
                elif not ghost.loop_size:
                    ghost.loop_size = step - ghost.first_end
        ghosts = [g for g in ghosts if not g.loop_size]
    return math.lcm(*[g.loop_size for g in all_ghosts])


data = get_data()

first = count_steps(*data)
second = count_steps_ghostly(*data)

print("First:  ", first)
print("Second: ", second)
