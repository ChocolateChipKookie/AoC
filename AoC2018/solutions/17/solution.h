//Advent of Code 2018 day 17
#ifndef AOC_17_H
#define AOC_17_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2018/solutions/17";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution(17, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution(17, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_17_H