//Advent of Code 2019 day 2
#ifndef AOC_02_H
#define AOC_02_H
#include "util.hpp"

std::string sourceDirectory = "../AoC2019/solutions/02";

// The original code did not include the intcode class
// For the original code check the other repo
void task_01(){
    auto inputs = loadIntcode(sourceDirectory + "/input");
    inputs[1] = 12;
    inputs[2] = 2;
    intcode interpreter(inputs);
    interpreter.run();
    print_solution(2, true, interpreter[0]);
}

void task_02(){
    auto inputs = loadIntcode(sourceDirectory + "/input");

    for(unsigned noun = 0; noun < inputs.size(); ++noun)
    {
        for (unsigned verb = 0; verb < inputs.size(); ++verb)
        {
            inputs[1] = noun;
            inputs[2] = verb;
            intcode interpreter(inputs);
            interpreter.run();
            if(interpreter[0] == 19690720){
                print_solution(2, false, noun * 100 + verb);
                return;
            }
        }
    }
}

int main(){
    task_01();
    task_02();
}

#endif //AOC_02_H
