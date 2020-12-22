#Advent of Code 2020 day 21
from util import *
DAY = 21

def get_data():
    lines = input_lines(DAY)
    res = [line.split('(contains ') for line in lines]
    res = [(x[0].split(), x[1][:-1].split(', ')) for x in res]
    return res

data = get_data()


allergens = set()
ingredients = set()
for food in data:
    ingredients.update(food[0])
    allergens  .update(food[1])

allergen_map = {x:set(ingredients) for x in allergens}

for allergen in allergens:
    # Find all food that contains that allergen
    contains_allergen = filter(lambda x: allergen in x[1], data)
    # Find intersection of all ingredients
    for food in contains_allergen:
        allergen_map[allergen] = allergen_map[allergen].intersection(food[0])

deducted = set()
while True:
    reducing = None

    for allergen in allergen_map:
        if allergen not in deducted:
            if len(allergen_map[allergen]) == 1:
                reducing = allergen
    if not reducing:
        break
    deducted.add(reducing)
    value = next(iter(allergen_map[reducing]))

    for allergen in allergen_map:
        if allergen != reducing:
            if value in allergen_map[allergen]:
                allergen_map[allergen].remove(value)

decoded_allergens = set(next(iter(allergen_map[x])) for x in allergen_map)

first = 0
for food in data:
    first += sum(1 for x in food[0] if x not in decoded_allergens)

second = ""
allergens = sorted(allergens)
for allergen in allergens:
    second += next(iter(allergen_map[allergen])) + ','
second = second[:-1]

print(f"First:  {first}")
print(f"Second: {second}")
