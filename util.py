import os
from aocd import get_data
import re
import datetime

YEAR = datetime.datetime.today().year


def get_input(day, year=YEAR, path=None):
    if path is None:
        path = f"AoC{year}/solutions/{str(day).zfill(2)}/input"

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


def set_output(first, second, day, year=YEAR, path=None):
    if path is None:
        path = f"AoC{year}/solutions/{str(day).zfill(2)}/output"

    out_file = open(path, 'w')
    out_file.write(
        f"""---Advent of Code {YEAR} day {day}---
First:  {first}
Second: {second}
"""
    )
    out_file.close()


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


def update_readme():
    """
        Updates README.md file for the git solution
        How it works:
            It reads the readme file, and looks for the marker in the file
            If it finds the marker, it writes from the position onwards
            If it doesn't it appends it to the file

            It looks for all the year files of format AoC2018, AoC2019, AoC2020...
            In that files there is a solutions folder with solutions for every solved day
            For a given year it lists out all the solutions in the given year's file
    """
    # Find years
    year_paths = sorted([(path, int(path[3:])) for path in os.listdir('.') if re.match("^AoC20\d{2}$", path)])

    # Define solution marker
    solutions_marker = "SOLUTIONS"
    marker_tag = f"<!{solutions_marker}>"
    # Create marker and marker caution
    marker_text = f"""{marker_tag}
<!-- Do not remove this lines, and write nothing after the {marker_tag} tag -->
<!--       They are used as marker for the generate_readme() function       -->"""

    # Default readme path name
    readme_path = "README.md"
    # Find readmes of any case
    readme_paths = [path for path in os.listdir('.') if re.match("^readme.md$", path, flags=re.IGNORECASE)]
    # If there are several readmes, raise error
    if len(readme_paths) > 1:
        raise ValueError("Too many README.md files!")
    # If there is only one readme, set the readme_path to the value
    if len(readme_paths) == 1:
        readme_path = readme_paths[0]

    # Read current readme
    with open(readme_path, 'r') as file:
        readme = file.read()

    with open(readme_path, 'r+') as readme_updated:
        # Finds marker position
        tag_pos = readme.find(marker_tag)
        # If it didn't find anything, append
        if tag_pos < 0:
            readme_updated.seek(len(readme))
        # Overwrite else
        else:
            readme_updated.seek(tag_pos)

        # Write marker text
        readme_updated.write(marker_text)
        # Start solutions section
        readme_updated.write("\n\n## Solutions")

        # For every year
        for file, year in year_paths:
            # Write what year it is
            readme_updated.write(f"\n\n### Year {year}\n")
            solutions_path = f"./{file}/solutions"
            # Find all solutions and sort them
            solution_dirs = sorted([(path, os.path.isfile(f"{solutions_path}/{path}/output")) for path in os.listdir(solutions_path) if re.match("^\d{2}$", path)])

            # For every day there is a solution for
            for day, has_output in solution_dirs:
                # link to the directory of the day
                day_dir = f"{solutions_path}/{day}"
                # Create entry for that day in format:
                readme_updated.write(f"\n* [Day {day}](https://adventofcode.com/{year}/day/{int(day)}) ([solution]({day_dir}))")


def generate_day(day, year=YEAR, download_input=True):
    filled = str(day).zfill(2)
    year_path = f"AoC{year}"
    solution_path = f"{year_path}/solutions"
    path = f"{solution_path}/{filled}"

    # Create directory for year
    if not os.path.isdir(f"AoC{YEAR}"):
        print(f"Creating directory for year {year}")
        os.mkdir(year_path)
    # Create directory for solutions
    if not os.path.isdir(f"AoC{YEAR}/solutions"):
        print(f"Creating solutions directory for year {year}")
        os.mkdir(solution_path)
    # Create directory for day
    if not os.path.isdir(path):
        print(f"Creating solutions directory for day {day}/{year}")
        os.mkdir(path)

    # Get input if enabled
    if download_input:
        print("Downloading input")
        get_input(day, year, path + "/input")

    # Create default output file
    if not os.path.isfile(path + "/output"):
        print("Creating output file")
        set_output("", "", day, year, path + "/output")
    # Create default Python file
    if not os.path.isfile(path + "/solution.py"):
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
    # Create default C++ file
    if not os.path.isfile(path + "/solution.h"):
        # Create c++ file
        print("Creating solution.h")
        cpp_file = open(path + "/solution.h", 'w')
        cpp_file.write(
            f"""//Advent of Code {YEAR} day {day}
#ifndef AOC_{filled}_H
#define AOC_{filled}_H
#include "../../../util.h"
#include <iostream>
#include <algorithm>

std::string sourceDirectory = "../AoC{year}/solutions/{filled}";

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
            f"""#include "{solution_path}/{filled}/solution.h"

int main() {{
    solution();
    //time_solution(solution);
    return 0;
}}
"""
        )
        cpp_main.close()
    # Create default Julia file
    if not os.path.isfile(path + "/solution.jl"):
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
    if not day:
        import datetime
        day = datetime.datetime.today().day

    generate_day(day, YEAR, True)
    update_readme()
