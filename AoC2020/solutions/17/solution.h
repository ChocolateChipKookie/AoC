//Advent of Code 2020 day 17
#ifndef AOC_17_H
#define AOC_17_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <map>

std::string sourceDirectory = "../AoC2020/solutions/17";

void printState(std::map<std::tuple<int, int, int>, bool>& values){
    std::pair<int, int> x_range, y_range, z_range;
    for(auto& key : values){
        if (key.second){
            x_range.first = std::min(x_range.first, std::get<0>(key.first));
            x_range.second = std::max(x_range.second, std::get<0>(key.first));
            y_range.first = std::min(y_range.first, std::get<1>(key.first));
            y_range.second = std::max(y_range.second, std::get<1>(key.first));
            z_range.first = std::min(z_range.first, std::get<2>(key.first));
            z_range.second = std::max(z_range.second, std::get<2>(key.first));
        }
    }

    for (int z = z_range.first - 1; z <= z_range.second + 1; ++z) {
        std::cout << "Z: " << z << "\n\n";
        for (int y = y_range.first - 1; y <= y_range.second + 1; ++y){
            for (int x = x_range.first - 1; x <= x_range.second + 1; ++x){
                std::cout << (values[{x, y, z}] ? '#' : '.');
            }
            std::cout << '\n';
        }
    }
    std::cout << std::endl;
}

void task_01(){
    auto data = loadLines(sourceDirectory + "/input");
    std::map<std::tuple<int, int, int>, bool> values;

    for (int y = 0; y < data.size(); ++y) {
        for (int x = 0; x < data[0].size(); ++x){
            values[{x, y, 0}] = data[y][x] == '#';
        }
    }

    for (int iter = 0; iter < 6; ++iter){
        std::pair<int, int> x_range, y_range, z_range;
        for(auto& key : values){
            if (key.second){
                x_range.first = std::min(x_range.first, std::get<0>(key.first));
                x_range.second = std::max(x_range.second, std::get<0>(key.first));
                y_range.first = std::min(y_range.first, std::get<1>(key.first));
                y_range.second = std::max(y_range.second, std::get<1>(key.first));
                z_range.first = std::min(z_range.first, std::get<2>(key.first));
                z_range.second = std::max(z_range.second, std::get<2>(key.first));
            }
        }

        auto new_map = values;
        for (int x = x_range.first - 1; x <= x_range.second + 1; ++x){
            for (int y = y_range.first - 1; y <= y_range.second + 1; ++y){
                for (int z = z_range.first - 1; z <= z_range.second + 1; ++z) {

                    int count = 0;
                    for (int dx = -1; dx <= 1; ++dx){
                        for (int dy = -1; dy <= 1; ++dy){
                            for (int dz = -1; dz <= 1; ++dz) {
                                if (dx == 0 && dy == 0 && dz == 0){
                                    continue;
                                }
                                if (values[{x + dx, y+dy, z+dz}]){
                                    ++count;
                                }
                            }
                        }
                    }

                    if (values[{x, y, z}]){
                        new_map[{x, y, z}] = (count == 2 || count == 3);
                    }
                    else {
                        new_map[{x, y, z}] = (count == 3);
                    }
                }
            }
        }
        values = new_map;
    }

    size_t res = 0;

    for (auto& a : values){
        if (a.second){
            ++res;
        }
    }

    print_solution(17, true, res);
}

void task_02(){
    auto data = loadLines(sourceDirectory + "/input");
    std::map<std::tuple<int, int, int, int>, bool> values;

    for (int y = 0; y < data.size(); ++y) {
        for (int x = 0; x < data[0].size(); ++x){
            values[{x, y, 0, 0}] = data[y][x] == '#';
        }
    }

    for (int iter = 0; iter < 6; ++iter){
        std::pair<int, int> x_range, y_range, z_range, w_range;
        for(auto& key : values){
            if (key.second){
                x_range.first = std::min(x_range.first, std::get<0>(key.first));
                x_range.second = std::max(x_range.second, std::get<0>(key.first));
                y_range.first = std::min(y_range.first, std::get<1>(key.first));
                y_range.second = std::max(y_range.second, std::get<1>(key.first));
                z_range.first = std::min(z_range.first, std::get<2>(key.first));
                z_range.second = std::max(z_range.second, std::get<2>(key.first));
                w_range.first = std::min(w_range.first, std::get<3>(key.first));
                w_range.second = std::max(w_range.second, std::get<3>(key.first));
            }
        }

        auto new_map = values;
        for (int x = x_range.first - 1; x <= x_range.second + 1; ++x){
            for (int y = y_range.first - 1; y <= y_range.second + 1; ++y){
                for (int z = z_range.first - 1; z <= z_range.second + 1; ++z) {
                    for (int w = w_range.first - 1; w <= w_range.second + 1; ++w) {
                        int count = 0;
                        for (int dx = -1; dx <= 1; ++dx){
                            for (int dy = -1; dy <= 1; ++dy){
                                for (int dz = -1; dz <= 1; ++dz) {
                                    for (int dw = -1; dw <= 1; ++dw) {
                                        if (dx == 0 && dy == 0 && dz == 0 && dw == 0){
                                            continue;
                                        }
                                        if (values[{x + dx, y+dy, z+dz, w+dw}]){
                                            ++count;
                                        }
                                    }
                                }
                            }
                        }

                        if (values[{x, y, z, w}]){
                            new_map[{x, y, z, w}] = (count == 2 || count == 3);
                        }
                        else {
                            new_map[{x, y, z, w}] = (count == 3);
                        }
                    }
                }
            }
        }
        values = new_map;
    }

    size_t res = 0;

    for (auto& a : values){
        if (a.second){
            ++res;
        }
    }

    print_solution(17, false, res);
}

void solution(){
    taks_01();
    taks_02();
}

#endif //AOC_17_H
