#Advent of Code 2022 day 7
from util import *
YEAR = 2022
DAY = 7

def get_data():
    return input_lines(DAY, YEAR)


data = get_data()

filesystem = {}


def from_path(path):
    if not path:
        return filesystem
    current = filesystem
    for token in path.split("/")[1:]:
        if not token:
            break
        current = current[token]
    return current


current_path = ""
ip = 0
while ip < len(data):
    line: str = data[ip]
    if line.startswith("$"):
        tokens = line.split()
        command = tokens[1]
        if command == "cd":
            if tokens[2] == "/":
                current_path = ""
            elif tokens[2] == "..":
                index = current_path.rfind("/")
                current_path = current_path[:index]
            else:
                current_path += f"/{tokens[2]}"
            ip += 1
        elif command == "ls":
            entries = []
            ip += 1
            while ip < len(data) and not data[ip].startswith("$"):
                entries.append(data[ip])
                ip += 1
            current_dir = from_path(current_path)
            for entry in entries:
                e_tokens = entry.split()
                if e_tokens[0] == "dir":
                    current_dir[e_tokens[1]] = {}
                else:
                    current_dir[e_tokens[1]] = int(e_tokens[0])

dir_sizes = []


def calc_size(file):
    if "__size__" in file:
        return file["__size__"]
    total_size = 0
    for entry in file:
        if isinstance(file[entry], int):
            total_size += file[entry]
        else:
            total_size += calc_size(file[entry])
    file["__size__"] = total_size
    dir_sizes.append(total_size)
    return total_size


def walk_first(file):
    if isinstance(file, (int, str)):
        return 0

    result = 0
    if file["__size__"] < 100000:
        result = file["__size__"]

    for entry in file:
        result += walk_first(file[entry])
    return result


calc_size(filesystem)
first = walk_first(filesystem)

max_final_size = 40_000_000
min_free = filesystem["__size__"] - max_final_size
dir_sizes.sort()
second = next(filter(lambda x: min_free < x, dir_sizes))

print("First:  ", first)
print("Second: ", second)