# Advent of Code 2023 day 20
from copy import deepcopy
from typing import Any
from util import *
from dataclasses import dataclass, field
import math

YEAR = 2023
DAY = 20


@dataclass
class Broadcast:
    outputs: list[str]
    name: str = "broadcaster"

    def __call__(self, queue, *_):
        for output in self.outputs:
            queue.append((output, False, self.name))


@dataclass
class FlipFlop:
    outputs: list[str]
    name: str
    state: bool = False

    def __call__(self, queue, high, _):
        if high:
            return
        self.state = not self.state
        for output in self.outputs:
            queue.append((output, self.state, self.name))


@dataclass
class Conjunction:
    outputs: list[str]
    name: str
    state: dict[str, bool] = field(default_factory=dict)

    def __call__(self, queue, high, name):
        self.state[name] = high
        out = not all(self.state.values())
        for output in self.outputs:
            queue.append((output, out, self.name))


@dataclass
class Output:
    name: str
    outputs: list[str] = field(default_factory=list)

    def __call__(self, *_):
        pass


def get_data():
    modules: dict[str, Any] = {}
    for line in input_lines(DAY, YEAR):
        if not line:
            continue
        l, r = line.split(" -> ")
        outputs = r.split(", ")
        if l == "broadcaster":
            modules[l] = Broadcast(outputs)
            continue
        t, n = l[0], l[1:]
        if t == "%":
            modules[n] = FlipFlop(outputs, n)
            continue
        if t == "&":
            modules[n] = Conjunction(outputs, n)
            continue
    output = "output"
    for name, module in modules.items():
        for o in module.outputs:
            if o not in modules:
                output = o
                continue
            target = modules[o]
            if isinstance(target, Conjunction):
                target.state[name] = False

    modules[output] = Output(output)
    return modules

def run():
    state = deepcopy(data)
    counts = {False: 0, True:0}
    for _ in range(1000):
        queue = [("broadcaster", False, "button")]
        while queue:
            target, signal, origin = queue.pop(0)
            counts[signal] += 1
            state[target](queue, signal, origin)
    return counts[True] * counts[False]

def run_rx():
    state = deepcopy(data)
    counter = 0
    final_module = None
    for module in state.values():
        if "rx" in module.outputs:
            final_module = module

    assert final_module is not None
    last_seen = {k: 0 for k in final_module.state}
    while True:
        queue = [("broadcaster", False, "button")]
        counter += 1
        while queue:
            target, signal, origin = queue.pop(0)
            state[target](queue, signal, origin)
            if target in final_module.state:
                if final_module.state[target] and not last_seen[target]:
                    last_seen[target] = counter
                    if all(v for v in last_seen.values()):
                        return math.lcm(*last_seen.values())


data = get_data()

first = run()
second = run_rx()

print("First:  ", first)
print("Second: ", second)
