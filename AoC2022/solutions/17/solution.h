//Advent of Code 2022 day 17
#ifndef AOC_17_H
#define AOC_17_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <set>
#include <map>

std::string sourceDirectory = "../AoC2022/solutions/17";

using int_t = long long;
const int_t width = 7;
using Position = std::array<int_t, 2>;
using Layer = std::array<char, width>;
const char EmptyVal = '.';
const char RockVal = '#';

std::vector<std::vector<Position>> rocks {
        std::vector<Position>{
                Position{0, 0},
                Position{1, 0},
                Position{2, 0},
                Position{3, 0},
        },
        std::vector<Position>{
                Position{1, 0},
                Position{0, 1},
                Position{1, 1},
                Position{2, 1},
                Position{1, 2},
        },
        std::vector<Position>{
                Position{0, 0},
                Position{1, 0},
                Position{2, 0},
                Position{2, 1},
                Position{2, 2},
        },
        std::vector<Position>{
                Position{0, 0},
                Position{0, 1},
                Position{0, 2},
                Position{0, 3},
        },
        std::vector<Position>{
                Position{0, 0},
                Position{1, 0},
                Position{0, 1},
                Position{1, 1},
        },
};

bool is_empty(const Layer& layer){
    return std::all_of(
            layer.begin(),
            layer.end(),
            [](char val){return val == '.';}
            );
}

Layer empty_layer(){
    Layer l;
    std::fill(l.begin(), l.end(), EmptyVal);
    return l;
}


int_t hash_layer(const Layer& layer){
    int_t mask = 1;
    int_t result = 0;

    for(auto c : layer){
        if (c == RockVal){
            result |= mask;
        }
        mask <<= 1;
    }
    return result;
}

void print(const std::vector<Layer>& layers, const Position& reference, size_t rock_id){
    std::set<Position> rock_positions;
    for (const auto& position : rocks[rock_id]){
        rock_positions.insert({
                                      reference[0] + position[0],
                                      reference[1] + position[1]
        });
    }

    for (size_t y = layers.size() - 1; y < layers.size(); --y){
        for (size_t x = 0; x < width; ++x){
            if (rock_positions.contains({x, y})){
                std::cout << '@';
                continue;
            }
            std::cout << layers[y][x];
        }
        std::cout << '\n';
    }
    std::cout << std::endl;
}

bool in_range(const Position& reference, size_t rock_id){
    for (auto& pos : rocks[rock_id]){
        int_t x = pos[0] + reference[0];
        if (x < 0 || x >= width){
            return false;
        }
    }
    return true;
}

bool collides(const Position& reference, size_t rock_id, const std::vector<Layer>& layers){
    for (auto& pos : rocks[rock_id]){
        int_t x = pos[0] + reference[0];
        int_t y = pos[1] + reference[1];
        if (y >= layers.size()){
            continue;
        }
        if (y < 0 || layers[y][x] == RockVal){
            return true;
        }
    }
    return false;
};


void task_01(const kki::string& input){
    std::vector<Layer> layers;
    layers.reserve(1000);
    for (int i = 0; i < 4; ++i){
        layers.push_back(empty_layer());
    }

    size_t jet_i = 0;
    size_t rock_id = 0;
    Position reference {2, layers.size() - 1};

    int_t rock_count = 0;
    int_t total_rocks = 2022;

    while (rock_count < total_rocks){
        int jet = input[jet_i] == '<' ? -1 : 1;
        jet_i = (jet_i + 1) % input.size();

        reference[0] += jet;
        if (!in_range(reference, rock_id) || collides(reference, rock_id, layers)){
            reference[0] -= jet;
        }

        reference[1] -= 1;
        if (collides(reference, rock_id, layers)){
            reference[1] += 1;
            for (auto& pos : rocks[rock_id]){
                int_t x = pos[0] + reference[0];
                int_t y = pos[1] + reference[1];
                layers[y][x] = RockVal;
            }

            while(!is_empty(layers[layers.size() - 4])){
                layers.push_back(empty_layer());
            }
            reference = {2, layers.size() - 1};
            rock_id = (rock_id + 1) % rocks.size();
            ++rock_count;
        }
    }

    print_solution(17, true, layers.size() - 4);
}

void task_02(const kki::string& input){
    std::vector<Layer> layers;
    layers.reserve(1000);
    for (int i = 0; i < 4; ++i){
        layers.push_back(empty_layer());
    }

    size_t jet_i = 0;
    size_t rock_id = 0;
    Position reference {2, layers.size() - 1};

    int_t rock_count = 0;
    int_t total_rocks = 1000000000000;

    std::map<std::array<int_t, 10>, std::array<int_t, 2>> states;
    int_t layers_skipped = 0;

    while (rock_count < total_rocks){
        int jet = input[jet_i] == '<' ? -1 : 1;
        ++jet_i;

        if (jet_i == input.size()) {
            jet_i = 0;
            if (layers_skipped == 0){
                std::array<int_t, 10> state {
                        rock_id,
                        layers.size() - reference[1],
                        reference[0],
                        hash_layer(layers[layers.size() - 4]),
                        hash_layer(layers[layers.size() - 5]),
                        hash_layer(layers[layers.size() - 6]),
                        hash_layer(layers[layers.size() - 7]),
                        hash_layer(layers[layers.size() - 8])
                };

                if (states.contains(state)){
                    int_t remaining_rocks = total_rocks - rock_count;
                    int_t period = rock_count - states[state][0];
                    int_t cycles_skipped = remaining_rocks / period;
                    layers_skipped = cycles_skipped * (layers.size() - states[state][1]);
                    rock_count += period * cycles_skipped;
                }
                else {
                    states[state] = {rock_count, layers.size()};
                }
            }
        }

        reference[0] += jet;
        if (!in_range(reference, rock_id) || collides(reference, rock_id, layers)){
            reference[0] -= jet;
        }

        reference[1] -= 1;
        if (collides(reference, rock_id, layers)){
            reference[1] += 1;
            for (auto& pos : rocks[rock_id]){
                int_t x = pos[0] + reference[0];
                int_t y = pos[1] + reference[1];
                layers[y][x] = RockVal;
            }

            while(!is_empty(layers[layers.size() - 4])){
                layers.push_back(empty_layer());
            }
            reference = {2, layers.size() - 1};
            rock_id = (rock_id + 1) % rocks.size();
            ++rock_count;
        }
    }

    print_solution(17, false, layers.size() - 4 + layers_skipped);
}

void solution(){
    auto line = loadLines(sourceDirectory + "/input")[0];

    task_01(line);
    task_02(line);
}

#endif //AOC_17_H