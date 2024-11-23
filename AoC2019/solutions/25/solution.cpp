//Advent of Code 2019 day 25
#ifndef AOC_25_H
#define AOC_25_H
#include <iostream>
#include <algorithm>
#include <iterator>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <array>

using lli = long long;
std::vector<lli> loadIntcode(const std::string& filepath){
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

std::string sourceDirectory = "../AoC2019/solutions/25";

class intcode
{
public:
    explicit intcode(std::string input_path = sourceDirectory + "/input") : input_file(std::move(input_path))
    {
        load();
    }

    void load()
    {
        inputs_ = loadIntcode(input_file);

        std::map<lli, lli> context;
        for (lli i = 0; i < inputs_.size(); ++i)
            context_[i] = inputs_[i];
        reset();
    }

    void reset()
    {
        i = relative = 0;
        context = context_;
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
            case 1: add(operands);							break;
            case 2: mul(operands);							break;
            case 3: input(operands, running, current_input);break;
            case 4: output(operands, running, outputs);		break;
            case 5: jump(operands, false);				break;
            case 6: jump(operands, true);				break;
            case 7: less(operands);							break;
            case 8: equal(operands);						break;
            case 9: add_relative(operands);					break;
            case 99: running = false;						break;
            default: throw std::runtime_error{ "Err" };
            }
        }
        return outputs;
    }

    //Input variables

    unsigned inputs = 0;

    inline void input(std::array<lli*, 3>& operands, bool& running, std::vector<lli>::iterator& in)
    {
        if (inputs == 0)
        {
            running = false;
            return;
        }

        *operands[0] = *in;
        ++in;
        i += 2;
        --inputs;
    }

    //Output variables

    inline void output(std::array<lli*, 3>& operands, bool& running, std::vector<lli>& outputs)
    {
        //OUTPUT
        if(*operands[0] < 128)
            std::cout << static_cast<char>(*operands[0]);
        else
            std::cout << *operands[0];

        i += 2;
    }

private:

    std::string input_file;
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


void task_01(){
    intcode ic;
    ic.inputs = 0;
    ic.run();
    while (true) {
        std::string instruction;
        std::getline(std::cin, instruction);

        std::vector<lli> program;

        for (char c : instruction)
        {
            program.emplace_back(static_cast<lli>(c));
        }
        program.emplace_back(static_cast<lli>('\n'));
        ic.inputs = program.size();
        ic.run(program);
    }
}

void task_02(){
}

/*
 * First: 34095120
 * Second: Press key
 *
 * Items : Planetoid, semiconductor, food, fixed point
 * LAYOUT:

                   *
                   |
   6-5-4-3-2-1 F H-I
     | | |     | |
   8-7 9 A-----E-G
         |       |
	   c-B       J
         |
		 D

* - GOAL
1 - Holodeck
2 - Stables
	Semiconductor
3 - Observatory
	planetoid
4 - Crew quarters
	food ration
5 - Sick Bay
	Fixed point
6 - Passages
	klein bottle
7 - Arcade
8 - Warp drive maintenence
	weather machine
9 - Storage
A - Kitchen
	giant electromagnet
B - Navigation
C - Science lab
	infinite loop
D - Hot chocolate fountain
	Pointer
E - Holodeck
	Coin
F - Hallway
	escape pod
G - Engineering
	photons
H - Gift wrapping
I - Security checkpoint
J - Corridor
	Molten lava
 */

int main() {
  task_01();
  task_02();
}

#endif //AOC_25_H
