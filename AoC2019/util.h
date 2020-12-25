//
// Created by kookie on 25. 12. 2020..
//

#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include <iostream>
#include <sstream>
#include <fstream>
#include <utility>
#include <vector>
#include <array>
#include <iterator>
#include <map>
#include <functional>
#include <chrono>


class intcode
{
public:
    using lli = long long;

    explicit intcode(std::vector<lli> data, bool print = false, bool blocking = false)
        :   inputs_(std::move(data)),
            print(print),
            blocking(blocking)
    {
        load();
    }

    void load()
    {
        for (lli j = 0; j < inputs_.size(); ++j)
            context_[j] = inputs_[j];
        reset();
    }

    void reset()
    {
        i = relative = 0;
        context = context_;
        halted = false;
    }

    std::vector<lli> run(std::vector<lli> inputs = {})
    {
        std::map<lli, lli>& input_code = context;
        auto current_input = inputs.begin();
        std::vector<lli> outputs;

        bool running = true;
        std::array<lli*, 3> operands{};
        while (running)
        {
            for (int k = 0; k < 3; ++k)
            {
                const int mode = nth_digit(input_code[i], k + 2);
                operands[k] = calculate_operand(input_code, mode, k + 1);
            }

            switch (input_code[i] % 100)
            {
            case 1: add(operands);break;
            case 2: mul(operands);break;
            case 3: input(operands, running, current_input);break;
            case 4: output(operands, running, outputs);break;
            case 5: jump(operands, false);break;
            case 6: jump(operands, true);break;
            case 7: less(operands);break;
            case 8: equal(operands);break;
            case 9: add_relative(operands);break;
            case 99: running = false; halted = true; break;
            default: throw std::runtime_error{ "Err" };
            }
        }
        return outputs;
    }

    lli operator[](lli pos){
        return context[pos];
    }

    //Input variables

    inline void input(std::array<lli*, 3>& operands, bool& running, std::vector<lli>::iterator& in)
    {
        *operands[0] = *in;
        ++in;
        i += 2;
    }

    //Output variables

    inline void output(std::array<lli*, 3>& operands, bool& running, std::vector<lli>& outputs)
    {
        //OUTPUT
        if(*operands[0] < 128){
            if (print){
                std::cout << static_cast<char>(*operands[0]);
            }
            outputs.push_back(*operands[0]);
        }
        else{
            if (print){
                std::cout << *operands[0];
            }
            outputs.push_back(*operands[0]);
        }
        if(blocking){
            running = false;
        }
        i += 2;
    }

    bool halted{false};
private:
    bool print = false;
    bool blocking = false;
    std::map<lli, lli> context;
    lli i{0}, relative{0};
    std::vector<lli> inputs_;
    std::map<lli, lli> context_;

    static inline int nth_digit(int number, int digit_number)
    {
        const auto pow_10 = [](unsigned pow)
        {
            int res = 1;
            for (unsigned i = 0; i < pow; ++i)res *= 10;
            return res;
        };
        return (number / pow_10(digit_number)) % 10;
    };

    inline lli* calculate_operand(std::map<lli, lli>& inputs, int mode, int operator_pos) const
    {
        switch (mode)
        {
        case 0: return &inputs[inputs[i + operator_pos]];
        case 1: return &inputs[i + operator_pos];
        case 2: return &inputs[relative + inputs[i + operator_pos]];
        default: return nullptr;
        }
    }

    inline void add(std::array<lli*, 3>& operands)
    {
        *operands[2] = *operands[0] + *operands[1];
        i += 4;
    }
    inline void mul(std::array<lli*, 3>& operands)
    {
        *operands[2] = (*operands[0]) * (*operands[1]);
        i += 4;
    }
    inline void jump(std::array<lli*, 3>& operands, bool zero)
    {
        if ((*operands[0] == 0) == zero)
            i = *operands[1];
        else
            i += 3;
    }
    inline void less(std::array<lli*, 3>& operands)
    {
        *operands[2] = *operands[0] < *operands[1];
        i += 4;
    }
    inline void equal(std::array<lli*, 3>& operands)
    {
        *operands[2] = *operands[0] == *operands[1];
        i += 4;
    }
    inline void add_relative(std::array<lli*, 3>& operands)
    {
        relative += *operands[0];
        i += 2;
    }
};


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

std::vector<long long int> loadIntcode(const std::string& filepath){
    std::ifstream ifs(filepath);
    if (!ifs.is_open()){
        throw std::invalid_argument("Path to input not valid!");
    }
    std::string str((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
    std::replace(str.begin(), str.end(), ',', ' ');
    std::stringstream ss(str);
    std::istream_iterator<long long int> begin(ss), end;
    std::vector<long long int> inputs{begin, end};
    ifs.close();
    return inputs;
}


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
