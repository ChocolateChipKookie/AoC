//Advent of Code 2019 day 1
#ifndef AOC_01_H
#define AOC_01_H
#include "util.hpp"
#include <iostream>
#include <algorithm>


std::string sourceDirectory = "../AoC2019/solutions/01";

void task_01(){
    std::vector<unsigned> inputs = loadTokens<unsigned>(sourceDirectory + "/input");
    unsigned res = 0;
    for (auto elem : inputs){
        unsigned val = elem / 3;
        val -= 2;
        res += val;
    }
    print_solution(1, true, res);
}

void task_02(){
    auto inputs = loadTokens<int>(sourceDirectory + "/input");
    int res{0};
    for (auto elem : inputs){
        while (true){
            elem /= 3;
            elem -= 2;
            if(elem <= 0) break;
            res += elem;
        }
    }
    print_solution(1, false, res);
}

int main() {
  task_01();
  task_02();
}

#endif //AOC_01_H
