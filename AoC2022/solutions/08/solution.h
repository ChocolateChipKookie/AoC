//Advent of Code 2022 day 8
#ifndef AOC_08_H
#define AOC_08_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>

std::string sourceDirectory = "../AoC2022/solutions/08";

void task_01(){
    IntGrid data = loadGrid<int>(sourceDirectory + "/input");
    IntGrid counts(data.size(), 0);

    for (size_t x = 0; x < data.size()[0]; ++x){
        int current_up = -1;
        int current_down = -1;

        for (size_t y = 0; y < data.size()[1]; ++y){
            size_t down_y = data.size()[1] - y - 1;
            if (data[x][y] > current_up){
                current_up = data[x][y];
                counts[x][y] = 1;
            }
            if (data[x][down_y] > current_down){
                current_down = data[x][down_y];
                counts[x][down_y] = 1;
            }
        }
    }
    for (size_t y = 0; y < data.size()[1]; ++y){
        int current_left = -1;
        int current_right = -1;

        for (size_t x = 0; x < data.size()[0]; ++x){
            size_t right_x = data.size()[0] - x - 1;
            if (data[x][y] > current_left){
                current_left = data[x][y];
                counts[x][y] = 1;
            }
            if (data[right_x][y] > current_right){
                current_right = data[right_x][y];
                counts[right_x][y] = 1;
            }
        }
    }

    const auto& counts_data = counts.data();
    int res = std::accumulate(counts_data.begin(), counts_data.end(), 0);
    print_solution(8, true, res);
}

int calc_score(IntGrid& data, size_t x, size_t y){
    int current_height = data[x][y];
    std::array<bool, 4> stopped {false};
    std::array<int, 4> visible {0};
    std::array<std::array<int, 2>, 4> directions{std::array<int, 2>{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

    for (int i = 1; i < std::max(data.size()[0], data.size()[1]); ++i){
        if (std::all_of(stopped.begin(), stopped.end(), [](bool b){return b;})){
            break;
        }

        for (size_t d = 0; d < directions.size(); ++d){
            auto [dx, dy] = directions[d];
            size_t nx = x + dx * i;
            size_t ny = y + dy * i;
            if (!stopped[d] && nx < data.size()[0] && ny < data.size()[1]){
                int height = data[nx][ny];
                visible[d] += 1;
                if (height >= current_height){
                    stopped[d] = true;
                }
            }
        }
    }
    return std::accumulate(visible.begin(), visible.end(), 1, [](int i1, int i2){return i1*i2;});
}

void task_02(){
    IntGrid data = loadGrid<int>(sourceDirectory + "/input");
    IntGrid scores(data.size(), 0);

    for (size_t x = 0; x < data.size()[0]; ++x){
        for (size_t y = 0; y < data.size()[1]; ++y){
            scores[x][y] = calc_score(data, x, y);
        }
    }

    const auto& counts_data = scores.data();
    int res = *std::max_element(counts_data.begin(), counts_data.end());
    print_solution(8, false, res);
}

void solution(){
    task_01();
    task_02();
}

#endif //AOC_08_H