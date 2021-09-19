//Advent of Code 2019 day 5
#ifndef AOC_05_H
#define AOC_05_H
#include "../../util.h"
#include <iostream>
#include <algorithm>

std::string sourceDirectory = "../AoC2019/solutions/05";

void task_01(){
    auto inputs = loadIntcode(sourceDirectory + "/input");
    intcode interpreter(inputs);
    auto out = interpreter.run({1});
    print_solution(5, true, out.back());
}

void task_02(){
    auto inputs = loadIntcode(sourceDirectory + "/input");
    intcode interpreter(inputs);
    auto out = interpreter.run({5});
    print_solution(5, false, out.back());
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_05_H
