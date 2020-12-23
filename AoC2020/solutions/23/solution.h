//Advent of Code 2020 day 23
#ifndef AOC_23_H
#define AOC_23_H
#include "../../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <memory>
#include <memory_resource>
#include <list>

std::string sourceDirectory = "../AoC2020/solutions/23";

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input")[0];
    int moves = 100;
    int current = 0;
    int data_size = data.length();
    int selected = 3;

    std::vector<char> copied(selected);

    for(int i = 0; i < moves; ++i){
        int value = data[current] - '0';
        // Because the values are from 1 to 9
        int value_dest;
        for (int j = 0; j < selected + 1; ++j){
            value_dest = ((value - 1 - j) + data_size - 1) % data_size + 1;
            bool valid = true;
            for (int k = 1; k <= selected; ++k){
                int cup_i = (current + k) % data_size;
                int cup = data[cup_i] - '0';
                if (cup == value_dest){
                    valid = false;
                    break;
                }
            }
            if (valid){
                break;
            }
        }
        int dest_i = data.find(value_dest + '0');

        for(int j = 0; j < selected; ++j){
            copied[j] = data[(i + 1 + j)%data_size];
        }

        for(int j = (i + 1)%data_size; (j + 3)%data_size != (dest_i + 1)%data_size; j = (j+1)%data_size){
            data[j] = data[(j+3)%data_size];
        }

        for(int j = 0; j < 3; ++j){
            data[(data_size + dest_i - 2 + j)%data_size] = copied[j];
        }
        current = (current + 1) % data_size;
    }

    std::string res(data_size-1, '0');
    size_t loc = (data.find('1') + 1) % data_size;
    for(unsigned i = 0; i < data_size - 1; ++i){
        res[i] = data[(loc + i)%data_size];
    }

    print_solution(23, true, res);
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input")[0];
    int cups = 1000000;
    int moves = 10000000;
    int selected = 3;

    // Create list from data
    std::list<int> list(data.begin(), data.end());
    for (int& item : list) {
        item -= '0';
    }
    // Fill the list to the brim
    while (list.size() != cups){
        list.push_back(list.size() + 1);
    }
    // Create lookup table
    std::vector<std::list<int>::iterator> locations(cups);
    // Fill lookup table
    for(auto i = list.begin(); i != list.end(); ++i){
        locations[*i - 1] = i;
    }

    // Set current pointer
    auto current = list.begin();
    // Define helper function for clockwise movement
    auto circularNext = [&list](const auto& it)
        {
            auto next = std::next(it);
            return next == list.end() ? list.begin() : next;
        };

    // Create buffer for storing selected cups
    std::vector<int> buffer(selected);

    for(int i = 0; i < moves; ++i){
        // Fetch selected and delete them
        for (int j = 0; j < 3; ++j){
            auto next = circularNext(current);
            buffer[j] = *next;
            list.erase(next);
        }

        // Get the destination value
        int value = *current;
        int dest = value - 1 == 0 ? cups : value - 1;
        while (true){
            if (std::find(buffer.begin(), buffer.end(), dest) == buffer.end()){
                break;
            }
            dest = dest - 1 == 0 ? cups : dest - 1;
        }

        // Find the destination iterator
        auto it = locations[dest - 1];

        // Increment by one as values are added before iterator
        ++it;
        // Add values from buffer and update lookup table
        for(auto elem : buffer){
            locations[elem-1] = list.insert(it, elem);
        }

        // Move to the next element
        current = circularNext(current);
    }

    // Fetch 2 values after 1
    auto one = std::find(list.begin(), list.end(), 1);
    one = circularNext(one);
    long long r1 = *one;
    one = circularNext(one);
    long long r2 = *one;
    // Result
    long long res = r1*r2;

    print_solution(23, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_23_H
