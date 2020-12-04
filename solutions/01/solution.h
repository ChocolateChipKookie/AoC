//
// Created by kookie on 01. 12. 2020..
//

#ifndef AOC_SOLUTION_H
#define AOC_SOLUTION_H
#include "../../util.h"
#include <iostream>
#include <set>
#include <algorithm>

void taks_01(const std::vector<size_t>& data){
    for (auto i1 : data){
        for (auto i2 : data){
            if( i1 + i2 == 2020){
                print_solution(1, true, i1 * i2);
                return;
            }
        }
    }
}

void taks_02(const std::vector<size_t>& data){
    for (auto i1 : data){
        for (auto i2 : data){
            for (auto i3 : data){
                if( i1 + i2 + i3 == 2020){
                    print_solution(1, false, i1 * i2 * i3);
                    return;
                }
            }
        }
    }
}

void solution(){
    auto data = loadTokens<size_t>("../solutions/day01/input");
    taks_01(data);
    taks_02(data);
}

#endif //AOC_SOLUTION_H
