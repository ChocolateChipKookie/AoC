//Advent of Code 2019 day 7
#ifndef AOC_07_H
#define AOC_07_H
#include "util.hpp"
#include <algorithm>

std::string sourceDirectory = "../AoC2019/solutions/07";

void task_01(){
    auto code = loadIntcode(sourceDirectory + "/input");
    intcode interpreter(code);
    long long max = 0;
    std::vector<long long> numbers{0, 1, 2, 3, 4};

    do{
        long long input = 0;
        for (auto phase : numbers){
            interpreter.reset();

            auto out = interpreter.run({phase, input});
            input = out[0];
        }
        max = std::max(max, input);
    }
    while (std::next_permutation(numbers.begin(), numbers.end()));

    print_solution(7, true, max);
}

void task_02(){
    auto code = loadIntcode(sourceDirectory + "/input");
    std::vector<intcode> interpreters;
    for(unsigned i = 0; i < 5; ++i){
        interpreters.emplace_back(code, false, true);
    }

    long long max = 0;
    std::vector<long long> phases{5, 6, 7, 8, 9};

    do{
        long long input = 0;
        // Prime the amplifiers
        for(unsigned i = 0; i < 5; ++i){
            interpreters[i].reset();
            input = interpreters[i].run({phases[i], input})[0];
        }

        while (true){
            bool halted = false;
            for(auto& interpreter : interpreters){
                auto out = interpreter.run({input});
                if (interpreter.halted){
                    halted = true;
                    break;
                }
                input = out[0];
            }
            if (halted){
                break;
            }
        }
        max = std::max(max, input);
    }
    while (std::next_permutation(phases.begin(), phases.end()));

    print_solution(7, false, max);
}

int main() {
  task_01();
  task_02();
}

#endif //AOC_07_H
