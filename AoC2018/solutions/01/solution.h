//Advent of Code 2018 day 1
#ifndef AOC_01_H
#define AOC_01_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <set>

std::string sourceDirectory = "../AoC2018/solutions/01";

void task_01(){
    auto data = loadTokens<int>(sourceDirectory + "/input");
    size_t res = std::accumulate(data.begin(),  data.end(), 0);
    print_solution(1, true, res);
}

void task_02(){
    auto data = loadTokens<int>(sourceDirectory + "/input");
    int current = 0;
    std::set<int> seen{current};

    while (true){
        for (auto val : data){
            current += val;
            if (seen.contains(current)){
                print_solution(1, false, current);
                return;
            }
            seen.insert(current);
        }
    }
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_01_H
