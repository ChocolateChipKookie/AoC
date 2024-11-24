//
// Created by kookie on 01. 12. 2020..
//

#ifndef AOC_UTIL_H
#define AOC_UTIL_H
#include <utility>
#include <vector>
#include <string>
#include <sstream>
#include <iterator>
#include <fstream>
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

std::vector<std::string> loadLines(const std::string& filepath, bool include_empty=false){
    std::ifstream ifs(filepath);
    std::string line;
    std::vector<std::string> inputs;
    while (std::getline(ifs, line)){
        if (include_empty || !line.empty()){
            inputs.push_back(line);
        }
    }
    return inputs;
}

class interpreter{
public:
    struct instruction{

        std::string operation{};
        std::vector<long long int> arguments{};
        explicit instruction(const std::string& ins){
            size_t pos = ins.find(' ');
            operation = ins.substr(0, pos);

            std::stringstream  ss(ins.substr(pos+1));
            std::istream_iterator<long long> begin(ss), end;
            std::copy(begin, end, std::back_inserter(arguments));
        }

        explicit instruction(std::string type, std::vector<long long> arguments)
                :   operation(std::move(type)),
                    arguments(std::move(arguments))
        {
        }

    };

    explicit interpreter(std::vector<instruction> instructions, long long accumulator = 0, long long pc = 0)
            :   instructions(std::move(instructions)),
                accumulator(accumulator),
                pc(pc)
    {
        setup();
    }

    explicit interpreter(const std::string& filepath, long long accumulator = 0, long long pc = 0)
        :   instructions(loadInstructions(filepath)),
            accumulator(accumulator),
            pc(pc)
    {
        setup();
    }

    static std::vector<instruction> loadInstructions(const std::string& filepath){
        std::vector<std::string> lines = loadLines(filepath);
        std::vector<instruction> instructions;
        instructions.reserve(lines.size());
        for ( auto& line : lines){
            instructions.emplace_back(line);
        }

        return instructions;
    }

    void setup(){
        // NOP
        functions["nop"] = [this](instruction& ins){
            ++pc;
        };
        // JMP
        functions["jmp"] = [this](instruction& ins){
            pc += ins.arguments[0];
        };
        functions["acc"] = [this](instruction& ins){
            accumulator += ins.arguments[0];
            pc++;
        };
    }

    int run_instruction(){
        if (terminated) return -1;
        instruction& ins = instructions[pc];
        functions[ins.operation](ins);
        if (pc >= instructions.size()){
            terminated = true;
            return 1;
        }
        std::unreachable();
    }

    long long int pc{0};
    long long int accumulator{0};
    std::vector<instruction> instructions;
    bool terminated{false};
private:
    std::unordered_map<std::string, std::function<void(instruction&)>> functions{};
};

template<typename T_res>
void print_solution(size_t day, bool easy, const T_res& result, const std::string& result_message = ""){
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
