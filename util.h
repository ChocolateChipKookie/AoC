//
// Created by kookie on 01. 12. 2020..
//

#ifndef AOC_UTIL_H
#define AOC_UTIL_H
#include <vector>
#include <string>
#include <sstream>
#include <iterator>
#include <fstream>
#include <tuple>
#include <functional>
#include <chrono>
#include <iostream>

template<typename T_token>
std::vector<T_token> loadTokens(const std::string& filepath){
    std::ifstream ifs(filepath);
    std::istream_iterator<T_token> begin(ifs), end;
    std::vector<T_token> inputs{begin, end };
    ifs.close();
    return inputs;
}

std::vector<std::string> loadLines(const std::string& filepath){
    std::ifstream ifs(filepath);
    std::string line;
    std::vector<std::string> inputs;
    while (std::getline(ifs, line)){
        inputs.push_back(line);
    }
    return inputs;
}

class interpreter{
public:
    enum class op{NOP, ACC, JMP};

    struct instruction{

        interpreter::op operation{};
        std::vector<long long int> arguments{};
        explicit instruction(const std::string& ins){
            size_t pos = ins.find(' ');
            std::string op_str = ins.substr(0, pos);

            if (op_str == "nop"){
                operation = interpreter::op::NOP;
            } else if (op_str == "acc") {
                operation = interpreter::op::ACC;
            } else if (op_str == "jmp"){
                operation = interpreter::op::JMP;
            } else {
                throw std::runtime_error("Operation not parsable!");
            }

            std::stringstream  ss(ins.substr(pos+1));
            std::istream_iterator<long long> begin(ss), end;
            std::copy(begin, end, std::back_inserter(arguments));
        }

        explicit instruction(interpreter::op type, std::vector<long long> arguments)
                :   operation(type),
                    arguments(std::move(arguments))
        {
        }

    };

    long long int pc{0};
    long long int accumulator{0};
    std::vector<instruction> instructions;
    bool terminated{false};

    explicit interpreter(const std::string& filepath, long long accumulator = 0, long long pc = 0)
        :   instructions(loadInstructions(filepath)),
            accumulator(accumulator),
            pc(pc)
    {}

    explicit interpreter(std::vector<instruction> instructions, long long accumulator = 0, long long pc = 0)
            :   instructions(std::move(instructions)),
                accumulator(accumulator),
                pc(pc)
    {}

    static std::vector<instruction> loadInstructions(const std::string& filepath){
        std::vector<std::string> lines = loadLines(filepath);
        std::vector<instruction> instructions;
        instructions.reserve(lines.size());
        for ( auto& line : lines){
            instructions.emplace_back(line);
        }

        return instructions;
    }

    int run_instruction(){
        if (terminated) return -1;

        instruction& ins = instructions[pc];
        switch (ins.operation) {
            case interpreter::op::NOP:
                pc++;
                break;
            case interpreter::op::ACC:
                accumulator += ins.arguments[0];
                pc++;
                break;
            case interpreter::op::JMP:
                pc += ins.arguments[0];
                break;
            default:
                throw std::runtime_error("Operation not implemented!");
        }
        if (pc >= instructions.size()){
            terminated = true;
            return 1;
        }
    }
};

void print_solution(size_t day, bool easy, size_t result, const std::string& result_message = ""){
    std::cout << "Day: " << day << "\nDifficulty: " << (easy ? "Easy" : "Hard") << "\nResult: ";
    if (!result_message.empty()){
        std::cout << result_message;
    }
    std::cout << result << std::endl;
}

void time_solution(const std::function<void(void)>& solution){
    auto begin = std::chrono::high_resolution_clock::now();
    solution();
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "\nTime elapsed: " << std::chrono::duration<double, std::milli>(end - begin).count() << " ms" << std::endl;
}

#endif //AOC_UTIL_H
