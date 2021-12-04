//Advent of Code 2021 day 1
#ifndef AOC_01_H
#define AOC_01_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2021/solutions/01";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(1, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(1, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_01_H
