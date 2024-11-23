//Advent of Code 2022 day 9
#ifndef AOC_09_H
#define AOC_09_H
#include "util.hpp"
#include <algorithm>
#include <set>
#include <map>

std::string sourceDirectory = "../AoC2022/solutions/09";

int max_dist(const std::array<int, 2>& p1, const std::array<int, 2>& p2){
    return std::max(std::abs(p1[0] - p2[0]), std::abs(p1[1] - p2[1]));
}

int min_dist(const std::array<int, 2>& p1, const std::array<int, 2>& p2){
    return std::min(std::abs(p1[0] - p2[0]), std::abs(p1[1] - p2[1]));
}

std::array<int, 2> move(std::array<int, 2>& knot, char direction){
    static const std::map<char, std::array<int, 2>> directions {
            {'U', { 0, 1}},
            {'D', { 0,-1}},
            {'L', {-1, 0}},
            {'R', { 1, 0}}
    };

    auto d = directions.at(direction);
    knot[0] += d[0];
    knot[1] += d[1];
    return d;
}

std::array<int, 2> adjust(const std::array<int, 2>& head, const std::array<int, 2>& prev_move, std::array<int, 2>& tail){
    std::array<int, 2> move {0, 0};
    if (max_dist(head, tail) > 1){
        if (std::abs(prev_move[0]) + std::abs(prev_move[1]) < 2){
            std::array<int, 2> new_pos {head[0] - prev_move[0], head[1] - prev_move[1]};
            move = {new_pos[0] - tail[0], new_pos[1] - tail[1]};
        }
        else if (min_dist(head, tail) == 0) {
            move = {head[0] - tail[0], head[1] - tail[1]};
            move[0] /= 2;
            move[1] /= 2;
        }
        else{
            move = prev_move;
        }
        tail[0] += move[0];
        tail[1] += move[1];
    }
    return move;
}

void task_01(const std::vector<std::pair<char, int>>& moves){
    std::array<int, 2> head_pos {0, 0};
    std::array<int, 2> tail_pos {0, 0};
    std::set<std::array<int, 2>> visited;
    visited.insert(tail_pos);

    for (auto [dir, dist] : moves){
        for (int i = 0; i < dist; ++i){
            auto m = move(head_pos, dir);
            adjust(head_pos, m, tail_pos);
            visited.insert(tail_pos);
        }
    }
    print_solution(9, true, visited.size());
}

void task_02(const std::vector<std::pair<char, int>>& moves){
    const int knots = 10;
    std::array<std::array<int, 2>, knots> rope {};
    std::set<std::array<int, 2>> visited;
    visited.insert(rope[0]);

    for (auto [dir, dist] : moves){
        for (int i = 0; i < dist; ++i){
            auto m = move(rope[0], dir);
            for (int k = 1; k < knots; ++k){
                m = adjust(rope[k - 1], m, rope[k]);
                if (m[0] == 0 && m[1] == 0){
                    break;
                }
            }
            visited.insert(rope.back());\
        }
    }
    print_solution(9, false, visited.size());
}

int main(){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    std::vector<std::pair<char, int>> moves;
    moves.reserve(data.size()/2);
    for (size_t i = 0; i < data.size(); i += 2){
        moves.emplace_back(data[i][0], std::stoi(data[i + 1]));
    }

    task_01(moves);
    task_02(moves);
}

#endif //AOC_09_H
