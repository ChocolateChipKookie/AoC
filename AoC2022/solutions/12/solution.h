//Advent of Code 2022 day 12
#ifndef AOC_12_H
#define AOC_12_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include "../../../util/array.h"
#include <unordered_set>
#include <queue>
#include <ranges>

std::string sourceDirectory = "../AoC2022/solutions/12";

using int_t = int;
using Position = std::array<int_t, 2>;
Position to_pos(const std::array<size_t, 2>& pos) {
    return {static_cast<int_t>(pos[0]), static_cast<int_t>(pos[1])};
};

namespace std{
    template<>
    struct hash<Position>{
        auto operator()(const Position& pos) const -> size_t {
            return pos[0] ^ (pos[0] + pos[1]);
        }
    };
}


const std::array<std::array<int, 2>, 4>& directions(){
    static std::array<std::array<int, 2>, 4> dirs {
            std::array{ 0, 1},
            std::array{ 1, 0},
            std::array{ 0,-1},
            std::array{-1, 0},
    };
    return dirs;
}

std::vector<Position>& expand_positions(const Position& current, CharGrid& grid, bool inverted = false){
    static std::vector<Position> results;
    results.reserve(4);
    results.clear();

    auto size = grid.size();
    char value = grid[current[0]][current[1]];
    for (auto& [dx, dy] : directions()){
        int_t nx = current[0] + dx;
        int_t ny = current[1] + dy;
        if (nx < 0 || nx >= size[0] || ny < 0 || ny >= size[1]) continue;

        char n_val = grid[nx][ny];
        if (!inverted && (n_val - value) > 1) continue;
        if (inverted && (value - n_val) > 1)
            continue;
        results.push_back({nx, ny});
    }
    return results;
}

struct Node {
    Position position;
    int_t distance = 0;
    int_t heuristic_distance = std::numeric_limits<int_t>::max();

    [[nodiscard]] int_t score() const {
        return distance + heuristic_distance;
    }
    [[nodiscard]] bool operator <(const Node& other) const{
        return score() > other.score();
    }
};


void task_01(CharGrid& data, Position start, Position end){
    auto h_dist = [&end](const Position& pos) -> int_t {
        return std::abs(end[0] - pos[0]) + std::abs(end[1] - pos[1]);
    };

    std::unordered_set<Position> visited;
    std::priority_queue<Node> to_visit;
    to_visit.push({start, 0, h_dist(start)});
    visited.insert(start);

    while (!to_visit.empty()){
        auto current = to_visit.top();
        to_visit.pop();
        visited.insert(current.position);
        for (auto& neighbour : expand_positions(current.position, data, false)){
            if (visited.contains(neighbour)) continue;
            if (neighbour == end){
                print_solution(12, true, current.distance + 1);
                return;
            }

            to_visit.push({neighbour, current.distance + 1, h_dist(neighbour)});
        }
    }
}

void task_02(CharGrid& data, Position end){
    auto& raw = data.data();
    std::unordered_set<Position> valid_positions;
    for (auto it = raw.begin(); it != raw.end(); ++it){
        if (*it == 'a'){
            valid_positions.insert(to_pos(data.get_position(it - raw.begin())));
        }
    }

    std::unordered_map<Position, int_t> h_dist_cache;
    h_dist_cache.reserve(valid_positions.size());
    auto h_dist = [&valid_positions, &h_dist_cache](const Position& pos) -> int_t {
        auto res_it = h_dist_cache.find(pos);
        if (res_it != h_dist_cache.end()){
            return res_it->second;
        }
        int_t res = std::numeric_limits<int_t>::max();

        for (auto& position : valid_positions){
            auto dist = std::abs(position[0] - pos[0]) + std::abs(position[1] - pos[1]);
            res = std::min(res, dist);
        }
        h_dist_cache[pos] = res;
        return res;
    };

    std::unordered_set<Position> visited;
    std::priority_queue<Node> to_visit;
    to_visit.push({end, 0, h_dist(end)});
    visited.insert(end);

    while (!to_visit.empty()){
        auto current = to_visit.top();
        to_visit.pop();
        visited.insert(current.position);
        for (auto& neighbour : expand_positions(current.position, data, true)){
            if (visited.contains(neighbour)) continue;
            auto current_distance = current.distance + 1;
            if (valid_positions.contains(neighbour)){
                print_solution(12, false, current_distance);
                return;
            }

            to_visit.push({neighbour, current_distance, h_dist(neighbour)});
        }
    }
}

void solution(){
    CharGrid data = loadGrid<char>(sourceDirectory + "/input");
    auto& raw = data.data();
    auto start_it = std::find(raw.begin(), raw.end(), 'S');
    auto end_it = std::find(raw.begin(), raw.end(), 'E');
    *start_it = 'a';
    *end_it = 'z';
    Position start = to_pos(data.get_position(start_it - raw.begin()));
    Position end = to_pos(data.get_position(end_it - raw.begin()));

    task_01(data, start, end);
    task_02(data, end);
}

#endif //AOC_12_H