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

template<typename T_res>
void print_solution(size_t day, bool easy, const T_res& result, const std::string& result_message = ""){
    std::cout << "Day: " << day << "\nDifficulty: " << (easy ? "Easy" : "Hard") << "\nResult: ";
    if (!result_message.empty()){
        std::cout << result_message;
    }
    std::cout << result << std::endl;
}

#endif //AOC_UTIL_H