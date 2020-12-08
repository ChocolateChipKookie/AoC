//Advent of Code 2020 day 8
#ifndef AOC_08_H
#define AOC_08_H
#include "../../../util.h"
#include <iostream>
#include <algorithm>
#include <set>

std::string sourceDirectory = "../AoC2020/solutions/08";

void taks_01(){
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

void taks_02(){
    std::vector<interpreter::instruction> instructions = interpreter::loadInstructions(sourceDirectory + "/input");
    std::vector<size_t> jumps;
    std::vector<size_t> nops;
    for (size_t i = 0; i < instructions.size(); ++i){
        switch (instructions[i].operation){
            case interpreter::op::JMP:
                jumps.push_back(i);
                break;
            case interpreter::op::NOP:
                nops.push_back(i);
                break;
            default:
                break;
        }
    }

    for (size_t jump : jumps){
        interpreter computer(instructions);
        computer.instructions[jump].operation = interpreter::op::NOP;

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
        computer.instructions[nop].operation = interpreter::op::JMP;

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
