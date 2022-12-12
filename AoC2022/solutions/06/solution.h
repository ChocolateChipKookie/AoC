//Advent of Code 2022 day 6
#ifndef AOC_06_H
#define AOC_06_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2022/solutions/06";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution(6, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution(6, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_06_H