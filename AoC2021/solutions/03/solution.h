//Advent of Code 2021 day 3
#ifndef AOC_03_H
#define AOC_03_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2021/solutions/03";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(3, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(3, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_03_H
