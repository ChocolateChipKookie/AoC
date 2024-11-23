//Advent of Code 2019 day 9
#ifndef AOC_09_H
#define AOC_09_H
#include "util.hpp"
#include <iostream>
#include <algorithm>

std::string sourceDirectory = "../AoC2019/solutions/09";

void task_01(){
    auto data = loadIntcode(sourceDirectory + "/input");
    intcode interpreter(data);
    auto out = interpreter.run({1});
    print_solution(9, true, out[0]);
}

void task_02(){
    auto data = loadIntcode(sourceDirectory + "/input");
    intcode interpreter(data);
    auto out = interpreter.run({2});
    print_solution(9, true, out[0]);
}

int main() {
  task_01();
  task_02();
}

#endif //AOC_09_H
