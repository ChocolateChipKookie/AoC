//Advent of Code 2018 day 9
#ifndef AOC_09_H
#define AOC_09_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <list>

std::string sourceDirectory = "../AoC2018/solutions/09";

using lli = long long;

lli play_game(lli players, lli last_value){
    std::list<lli> game_state{0};
    std::vector<lli> scores(players, 0);
    auto current_marble = game_state.begin();
    auto inc = [&](){
        ++current_marble;
        if (current_marble == game_state.end()){
            current_marble = game_state.begin();
        }
    };
    auto dec = [&](){
        if (current_marble == game_state.begin()){
            current_marble = game_state.end();
        }
        --current_marble;
    };
    auto move = [&](lli n){
        if (n > 0)
            for (lli i = 0; i < n; ++i) inc();
        else
            for (lli i = 0; i < -n; ++i) dec();
    };

    for (lli current_value = 1; current_value <= last_value; ++current_value){
        if (current_value % 23 == 0){
            move(-7);
            scores[(current_value - 1) % players] += current_value;
            scores[(current_value - 1) % players] += *current_marble;
            current_marble = game_state.erase(current_marble);
        }
        else{
            move(2);
            current_marble = game_state.insert(current_marble, current_value);
        }
    }

    return *std::max_element(scores.begin(),  scores.end());
}

void task_01(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    const lli players = std::stoll(data[0]);
    const lli last_value = std::stoll(data[6]);
    print_solution(9, true, play_game(players, last_value));
}

void task_02(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    const lli players = std::stoll(data[0]);
    const lli last_value = std::stoll(data[6]) * 100;
    print_solution(9, false, play_game(players, last_value));
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_09_H
