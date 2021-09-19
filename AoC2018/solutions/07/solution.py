#Advent of Code 2018 day 7
from util import *
DAY = 7
YEAR = 2018

def get_data():
    return input_lines(DAY, YEAR)

data = get_data()
data = [x.split() for x in data]
data = [(x[1], x[7]) for x in data]


class Recipe:
    def __init__(self, steps):
        self.steps = list(steps)
        self.uncompleted = set([x[0] for x in steps] + [x[1] for x in steps])
        self.completed = []
        self.available = []

    def is_possible(self, step):
        for requirement in self.steps:
            if step == requirement[1]:
                return False
        return True

    def check_possible(self):
        self.available = []
        for step in self.uncompleted:
            if self.is_possible(step):
                self.available.append(step)
        self.available.sort()
        return self.available

    def complete_step(self, step):
        self.completed.append(step)
        self.uncompleted.remove(step)
        self.steps = [x for x in self.steps if x[0] != step]


class ComplicatedRecipe:
    def __init__(self, steps, offset, workers):
        self.steps = list(steps)
        self.workers = workers
        self.uncompleted = set([x[0] for x in steps] + [x[1] for x in steps])
        self.time_map = {x: (offset + 1 + ord(x) - ord('A')) for x in self.uncompleted}
        self.completed = []
        self.executing = []
        self.available = []
        self.assign_tasks()
        self.time_step = 0

    def is_possible(self, step):
        for requirement in self.steps:
            if step == requirement[1]:
                return False
        return True

    def check_possible(self):
        self.available = []
        executing = [x[0] for x in self.executing]
        for step in self.uncompleted:
            if self.is_possible(step) and step not in executing:
                self.available.append(step)
        self.available.sort()
        return self.available

    def complete_step(self, step):
        self.completed.append(step)
        self.uncompleted.remove(step)
        self.steps = [x for x in self.steps if x[0] != step]

    def assign_tasks(self):
        if self.workers > 0:
            possible = self.check_possible()
            for i in possible:
                if self.workers == 0:
                    break
                self.executing.append([i, self.time_map[i]])
                self.workers -= 1

    def step(self):
        self.time_step += 1
        for task in self.executing:
            task[1] -= 1
            if task[1] == 0:
                self.complete_step(task[0])
                self.workers += 1
        self.assign_tasks()
        self.executing = [x for x in self.executing if x[1] > 0]


recipe = Recipe(data)
while len(recipe.uncompleted) > 0:
    possible = recipe.check_possible()
    recipe.complete_step(possible[0])

complicated_recipe = ComplicatedRecipe(data, offset = 60, workers=5)
while len(complicated_recipe.uncompleted) > 0:
    complicated_recipe.step()


first = "".join(recipe.completed)
second = complicated_recipe.time_step

print(f"First:  {first}")
print(f"Second: {second}")
