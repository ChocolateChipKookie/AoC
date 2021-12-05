//Advent of Code {year} day {day}
#ifndef AOC_{filled}_H
#define AOC_{filled}_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC{year}/solutions/{filled}";

void task_01(){{
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution({day}, true, res);
}}

void task_02(){{
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution({day}, false, res);
}}

void solution(){{
    task_01();
    task_02();
}}

#endif //AOC_{filled}_H