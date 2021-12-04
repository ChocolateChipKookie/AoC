//Advent of Code 2021 day 4
#ifndef AOC_04_H
#define AOC_04_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2021/solutions/04";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(4, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};

    print_solution(4, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_04_H
