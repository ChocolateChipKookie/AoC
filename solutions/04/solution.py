#Advent of Code 2020 day 4
from util import *
import string
DAY = 4

def get_data():
    data = get_input(DAY).strip()
    data = [x.strip().split() for x in data.split('\n\n')]
    data = [[x.strip().split(":") for x in y] for y in data]
    data = [{x[0]:x[1] for x in y} for y in data]
    return list(data)

data = get_data()

def isValid1(password):
    parameters = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all([(param in password) for param in parameters])

def isValid2(password):
    parameters = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    if not all([(param in password) for param in parameters]):
        return False

    def tryValid(password):
        if not (1920 <= int(password["byr"]) <= 2002):
            return False
        if not (2010 <= int(password["iyr"]) <= 2020):
            return False
        if not (2020 <= int(password["eyr"]) <= 2030):
            return False
        if password["hgt"][-2:] == "in":
            if not (59 <= int(password["hgt"][:-2]) <= 76):
                return False
        elif password["hgt"][-2:] == "cm":
            if not (150 <= int(password["hgt"][:-2]) <= 193):
                return False
        else:
            return False

        if not (password["hcl"][0] == '#' and
                len(password["hcl"]) == 7 and
                all(c in string.hexdigits for c in password["hcl"][1:])):
            return False

        if password["ecl"] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False

        if not (password["pid"].isdecimal() and len(password["pid"]) == 9):
            return False

        return True

    try:
        return tryValid(password)
    except:
        return False

first = sum(1 for x in data if isValid1(x))
second = sum(1 for x in data if isValid2(x))

print(f"First:  {first}")
print(f"Second: {second}")
