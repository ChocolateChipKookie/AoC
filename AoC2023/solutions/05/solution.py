#Advent of Code 2023 day 5
from util import *
YEAR = 2023
DAY = 5

Mapping = list[tuple[int, int, int]]
Range = tuple[int, int]

def get_data() -> tuple[list[int], list[Mapping]]:
    lines = input_lines(DAY, YEAR)
    seeds = [int(i) for i in lines[0].split(":")[1].strip().split()]

    mappings: list[Mapping] = []

    for line in lines[1:]:
        if not line:
            continue
        if "map" in line:
            mappings.append([])
            continue
        d, s, l = (int(i) for i in line.split())
        mappings[-1].append((d, s, l))

    return seeds, mappings

def seed_to_location(seed: int, mappings: list[Mapping]) -> int:
    current_value = seed
    def map_value(val: int, ms: Mapping) -> int:
        for dest, src, l in ms:
            if val in range(src, src + l):
                return dest + (val - src)
        return val

    for m in mappings:
        current_value = map_value(current_value, m)
    return current_value


def seed_to_location_ranged(seed: Range, mappings: list[Mapping]) -> list[Range]:
    def map_range(range_: Range, mapping: Mapping)-> list[Range]:
        current, range_end = range_
        res = []
        while current < range_end:
            found_mapping = False
            for dest, src, l in mapping:
                src_end = src + l
                if current in range(src, src_end):
                    current_offset = current - src
                    start = dest + current_offset
                    current_len = min(l - current_offset, (range_end - current))
                    res.append((start, start + current_len))
                    current += current_len
                    found_mapping = True
                    continue
            if not found_mapping:
                filtered_mappings = [m for m in mapping if m[1] > current]
                if not filtered_mappings:
                    res.append((current, range_end))
                    break
                end = min(m[1] for m in filtered_mappings)
                res.append((current, end))
                current = end
                pass

        return res

    ranges = [seed]
    for m in mappings:
        new_ranges = []
        for r in ranges:
            new_ranges.extend(map_range(r, m))
        ranges = new_ranges
    return ranges

seeds, mappings = get_data()

first = min(seed_to_location(s, mappings) for s in seeds)
seed_ranges = [(s, s+l) for s, l in zip(seeds[0::2], seeds[1::2])]
resulting_ranges = [seed_to_location_ranged(sr, mappings) for sr in seed_ranges]
second = min(min(r[0] for r in rr) for rr in resulting_ranges)

print("First:  ", first)
print("Second: ", second)
