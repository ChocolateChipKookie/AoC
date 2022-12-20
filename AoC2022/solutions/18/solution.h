//Advent of Code 2022 day 18
#ifndef AOC_18_H
#define AOC_18_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <map>
#include <set>

std::string sourceDirectory = "../AoC2022/solutions/18";
using int_t = long long;
using Position = std::array<int_t, 3>;

bool connected(const Position& p1, const Position& p2){
    int_t distance =
            std::abs(p1[0] - p2[0]) +
            std::abs(p1[1] - p2[1]) +
            std::abs(p1[2] - p2[2]);
    return distance == 1;
}

void task_01(std::vector<Position>& positions){
    size_t res = 0;

    for (int i = 0; i < positions.size(); ++i){
        res += 6;
        auto& pi = positions[i];
        for (int j = i + 1; j < positions.size(); ++j){
            if (connected(pi, positions[j])){
                res -= 2;
            }
        }
    }

    print_solution(18, true, res);
}

void task_02(std::vector<Position>& positions){
    size_t res = 0;
    std::map<Position, int_t> air;
    std::set<Position> droplets;

    std::array<std::array<int_t, 3>, 6> directions {
            std::array<int_t, 3>{ 0, 0, 1},
            std::array<int_t, 3>{ 0, 0,-1},
            std::array<int_t, 3>{ 0, 1, 0},
            std::array<int_t, 3>{ 0,-1, 0},
            std::array<int_t, 3>{ 1, 0, 0},
            std::array<int_t, 3>{-1, 0, 0}
    };

    Position min = positions[0];
    Position max = positions[0];
    auto update_minmax = [&](const Position& p){
        for (int i = 0; i < 3; i ++){
            min[i] = std::min(p[i], min[i]);
            max[i] = std::max(p[i], max[i]);
        }
    };

    // Find minmax and all potential air positions
    for (int i = 0; i < positions.size(); ++i){
        res += 6;
        auto& pi = positions[i];
        update_minmax(pi);
        droplets.insert(pi);

        for (auto& direction : directions){
            Position pa = {
                    pi[0] + direction[0],
                    pi[1] + direction[1],
                    pi[2] + direction[2],
            };
            air[pa] += 1;
        }
        for (int j = i + 1; j < positions.size(); ++j){
            if (connected(pi, positions[j])){
                res -= 2;
            }
        }
    }

    // Store all unreachable positions
    std::set<Position> unreachable;
    // Check if a position is reachable from outside with a breadth first search
    auto reachable = [&](const Position& p, int_t count) -> bool{
        if (count == 6 || unreachable.contains(p)){
            return false;
        }
        if (to_outside(p) <= 0){
            return true;
        }

        auto to_outside = [&](const Position& p) -> int_t {
            int_t min_distance = std::numeric_limits<int_t>::max();
            for (int i = 0; i < 3; ++i){
                min_distance = std::min(p[i] - min[i], min_distance);
                min_distance = std::min(max[i] - p[i], min_distance);
            }
            return min_distance;
        };

        static std::vector<Position> to_expand;
        to_expand.clear();
        to_expand.push_back(p);
        static std::set<Position> visited;
        visited.clear();
        size_t current_i = 0;

        while (current_i < to_expand.size()){
            Position current = to_expand[current_i++];
            for (const auto& direction : directions){
                Position npos = {
                        current[0] + direction[0],
                        current[1] + direction[1],
                        current[2] + direction[2]
                };
                if (droplets.contains(npos) || visited.contains(npos)){
                    continue;
                }
                if (unreachable.contains(npos)){
                    unreachable.insert(visited.begin(), visited.end());
                    return false;
                }
                if (to_outside(npos) == 0){
                    return true;
                }
                visited.insert(npos);
                to_expand.push_back(npos);
            }
        }
        unreachable.insert(visited.begin(), visited.end());
        return false;
    };

    // Update result
    for (auto& [pa, count] : air){
        if (!droplets.contains(pa) && !reachable(pa, count)){
            res -= count;
        }
    }

    print_solution(18, false, res);
}

void solution(){
    auto lines = loadLines(sourceDirectory + "/input");
    auto parse = [](const kki::string& str){
        int_t result;
        std::from_chars(str.begin(), str.end(), result);
        return result;
    };

    std::vector<Position> positions;
    positions.reserve(lines.size());
    for (const auto& line : lines){
        auto tokens = line.split(',');
        positions.push_back(Position{
                parse(tokens[0]),
                parse(tokens[1]),
                parse(tokens[2])
        });
    }

    task_01(positions);
    task_02(positions);
}

#endif //AOC_18_H