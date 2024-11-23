//Advent of Code 2020 day 9
#ifndef AOC_09_H
#define AOC_09_H
#include "util.hpp"
#include <algorithm>

std::string sourceDirectory = "../AoC2020/solutions/09";
size_t first = 0;

void task_01(){
    auto data = loadTokens<size_t>(sourceDirectory + "/input");
    unsigned range = 25;
    for (unsigned i = 0; i < data.size(); ++i){
        bool found = false;
        for (unsigned x = 0; x < range && !found; ++x){
            for (unsigned y = 0; y < range && !found; ++y) {
                auto dx=data[i + x], dy=data[i + y];
                if (dx != dy){
                    if (dx+dy == data[i+range]){
                        found = true;
                    }
                }
            }
        }
        if(!found){
            first = data[i + range];
            print_solution(9, true, first);
            return;
        }
    }

}

void task_02(){
    auto data = loadTokens<size_t>(sourceDirectory + "/input");
    for (auto i = data.begin(); i != data.end(); ++i){
        size_t sum = 0;
        for (unsigned j = 0;; ++j){
            sum += i[j];
            if (sum > first){
                break;
            }
            if (sum == first){
                auto min = *std::min_element(i, i+j+1);
                auto max = *std::max_element(i, i+j+1);
                print_solution(9, false, min+max);
                return;
            }
        }
    }

}

int main(){
    task_01();
    task_02();
}

#endif //AOC_09_H
