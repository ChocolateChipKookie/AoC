import os.path
from aocd import get_data
import re

YEAR = 2020


def get_input(day, year=YEAR):
    path = "solutions/" + str(day).zfill(2) + '/input'

    if year == YEAR:
        if os.path.isfile(path):
            return open(path, 'r').read()
        else:
            puzzle_input = get_data(day=day, year=year)
            file = open(path, 'w')
            file.write(puzzle_input)
            file.close()
            return puzzle_input
    else:
        return get_data(day=day, year=year)


def get_lines(string):
    return [x.strip() for x in string.strip().split('\n')]


def input_lines(day):
    return get_lines(get_input(day))


def get_integers(string):
    return list(map(int, re.findall(r'\d+', string)))


def input_integers(day):
    return get_integers(get_input(day))


def input_tokens(day, delim=None):
    return [x.strip() for x in get_input(day).strip().split(delim)]


def generate_day(day, download_input=False):
    filled = str(day).zfill(2)
    path = "solutions/" + filled
    print(f"Generating directory for day {filled}!")

    if os.path.isdir(path):
        raise ValueError("File structure already exists")
    else:
        # Create directory
        print("Creating directory")
        os.mkdir(path)
        # Get input if enabled
        if download_input:
            print("Downloading input")
            get_input(day)

        # Create python file
        print("Creating solution.py")
        py_file = open(path + "/solution.py", 'w')
        py_file.write(
            f"""#Advent of Code {YEAR} day {day}
from util import *
DAY = {day}

def get_data():
    return input_lines(DAY)

data = get_data()

first = None
second = None

print(f"First:  {{first}}")
print(f"Second: {{second}}")
"""
        )
        py_file.close()

        # Create c++ file
        print("Creating solution.h")
        cpp_file = open(path + "/solution.h", 'w')
        cpp_file.write(
            f"""//Advent of Code {YEAR} day {day}
#ifndef AOC_{filled}_H
#define AOC_{filled}_H
#include "../../util.h"
#include <iostream>
#include <algorithm>

std::string sourceDirectory = "../solutions/{filled}";

void taks_01(){{
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{{0}};

    print_solution({day}, true, res);
}}

void taks_02(){{
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{{0}};

    print_solution({day}, false, res);
}}

void solution(){{
    taks_01();
    taks_02();
}}

#endif //AOC_{filled}_H
"""
        )
        cpp_file.close()

        print("Modifying main.cpp")
        # Modify c++ main
        cpp_main = open("main.cpp", 'w')
        cpp_main.write(
            f"""#include "solutions/{filled}/solution.h"

int main() {{
    solution();
    //time_solution(solution);
    return 0;
}}
"""
        )
        cpp_main.close()

        print("Creating solution.jl")
        jl_file = open(path + "/solution.jl", 'w')
        jl_file.write(
            f"""#Advent of Code {YEAR} day {day}
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\\n")
    return lines
end

function task1(data)
    return Nothing
end
    
function task2(data)
    return Nothing
end


function solution()
    data = load()
    #println(data)
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end
    
solution()
"""
        )
        jl_file.close()


if __name__ == "__main__":
    day = None  # Override here
    if day is None:
        import datetime
        day = datetime.datetime.today().day

    generate_day(day, True)
