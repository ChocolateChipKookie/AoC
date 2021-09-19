#Advent of Code 2020 day 4
from util import *
import string
DAY = 4
YEAR = 2020


def get_data():
    data = get_input(DAY, YEAR).strip()
    data = [x.strip().split() for x in data.split('\n\n')]
    data = [[x.strip().split(":") for x in y] for y in data]
    data = [{x[0]:x[1] for x in y} for y in data]
    return list(data)

data = get_data()

def isValid1(password):
    parameters = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all([(param in password) for param in parameters])

def isValid2(password):
    try:
        # Birth year
        if not (1920 <= int(password["byr"]) <= 2002):
            return False
        # Issue year
        if not (2010 <= int(password["iyr"]) <= 2020):
            return False
        # Expiry year
        if not (2020 <= int(password["eyr"]) <= 2030):
            return False
        # Height ends in inches or cm and values are good
        if password["hgt"][-2:] == "in":
            if not (59 <= int(password["hgt"][:-2]) <= 76):
                return False
        elif password["hgt"][-2:] == "cm":
            if not (150 <= int(password["hgt"][:-2]) <= 193):
                return False
        else:
            return False
        # Hair colour
        if not (password["hcl"][0] == '#' and all(c in string.hexdigits for c in password["hcl"][1:7])):
            return False
        # Eye colour
        if password["ecl"] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False
        # Personal identification number
        if not (password["pid"].isdecimal() and len(password["pid"]) == 9):
            return False
        # Finally true
        return True
    except:
        # If it throws any error, it is not as parsable as it should be
        return False

first = sum(1 for x in data if isValid1(x))
second = sum(1 for x in data if isValid2(x))

print(f"First:  {first}")
print(f"Second: {second}")
