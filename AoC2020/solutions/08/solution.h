//Advent of Code 2020 day 8
#ifndef AOC_08_H
#define AOC_08_H
#include "../../../util.h"
#include <iostream>
#include <algorithm>
#include <set>

std::string sourceDirectory = "../AoC2020/solutions/08";

void task_01(){
    interpreter computer(sourceDirectory + "/input");
    std::set<long long int> visited_instructions{computer.pc};
    long long int res;
    while (true){
        computer.run_instruction();
        if (visited_instructions.contains(computer.pc)){
            res = computer.accumulator;
            break;
        }
        visited_instructions.insert(computer.pc);
    }

    print_solution(8, true, res);
}

void task_02(){
    std::vector<interpreter::instruction> instructions = interpreter::loadInstructions(sourceDirectory + "/input");
    std::vector<size_t> jumps;
    std::vector<size_t> nops;
    for (size_t i = 0; i < instructions.size(); ++i){
        if (instructions[i].operation == "jmp"){
            jumps.push_back(i);
        }
        else if (instructions[i].operation == "nop"){
            nops.push_back(i);
        }
    }

    for (size_t jump : jumps){
        interpreter computer(instructions);
        computer.instructions[jump].operation = "nop";

        std::set<long long int> visited_instructions{computer.pc};
        while (true){
            computer.run_instruction();
            if (visited_instructions.contains(computer.pc)){
                break;
            }
            if (computer.terminated){
                print_solution(8, false, computer.accumulator);
                return;
            }

            visited_instructions.insert(computer.pc);
        }
    }

    for (size_t nop : nops){
        interpreter computer(instructions);
        computer.instructions[nop].operation = "jmp";

        std::set<long long int> visited_instructions{computer.pc};
        while (true){
            computer.run_instruction();
            if (visited_instructions.contains(computer.pc)){
                break;
            }
            if (computer.terminated){
                print_solution(8, false, computer.accumulator);
                return;
            }

            visited_instructions.insert(computer.pc);
        }
    }

}

void solution(){
    taks_01();
    taks_02();
}

#endif //AOC_08_H
