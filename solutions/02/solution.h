//
// Created by kookie on 01. 12. 2020..
//

#ifndef AOC_01_H
#define AOC_01_H
#include "../../util.h"
#include <iostream>
#include <algorithm>

std::string sourceDirectory = "../solutions/02";

void taks_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};
    for (int i = 0; i < data.size(); i += 3) {
        // Parse data
        auto &t1 = data[i + 0];
        size_t pos = t1.find('-');
        // First and second number
        size_t first = std::stoi(t1.substr(0, pos));
        size_t second = std::stoi(t1.substr(pos + 1));
        // Value and password
        auto value = data[i + 1][0];
        auto &password = data[i + 2];

        size_t occurances = std::count(password.begin(), password.end(), value);
        if (first <= occurances && occurances <= second) {
            res++;
        }
    }
    print_solution(2, true, res);
}

void taks_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res{0};
    for (int i = 0; i < data.size(); i += 3){
        auto &t1 = data[i + 0];
        size_t pos = t1.find('-');
        // One indexed
        size_t first = std::stoi(t1.substr(0, pos)) - 1;
        size_t second = std::stoi(t1.substr(pos + 1)) - 1;

        auto value = data[i + 1][0];
        auto &password = data[i + 2];

        if ((password[first] == value) != (password[second] == value)) {
            res++;
        }
    }
    print_solution(2, false, res);
}

void solution(){
    taks_01();
    taks_02();
}

#endif //AOC_01_H
