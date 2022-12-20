//Advent of Code 2022 day 19
#ifndef AOC_19_H
#define AOC_19_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <array>

std::string sourceDirectory = "../AoC2022/solutions/19";

using int_t = long long;
enum Resource : int_t {
    Ore      = 0,
    Clay     = 1,
    Obsidian = 2,
    Geode    = 3,
    None     = -1,
};

struct Blueprint{
    explicit Blueprint(const kki::string& blueprint){
        auto tokens = blueprint.split();
        auto id_start = blueprint.find(' ') + 1;
        auto id_end = blueprint.find(':');

        std::from_chars(blueprint.begin() + id_start, blueprint.begin() + id_end, id);

        std::from_chars(tokens[6].begin(), tokens[6].end(), costs[Resource::Ore][Resource::Ore]);
        std::from_chars(tokens[12].begin(), tokens[12].end(), costs[Resource::Clay][Resource::Ore]);
        std::from_chars(tokens[18].begin(), tokens[18].end(), costs[Resource::Obsidian][Resource::Ore]);
        std::from_chars(tokens[21].begin(), tokens[21].end(), costs[Resource::Obsidian][Resource::Clay]);
        std::from_chars(tokens[27].begin(), tokens[27].end(), costs[Resource::Geode][Resource::Ore]);
        std::from_chars(tokens[30].begin(), tokens[30].end(), costs[Resource::Geode][Resource::Obsidian]);


        for (int i = 0; i < 4; ++i){
            max_requirements[i] = 0;
            for (int j = 0; j < 4; ++j){
                max_requirements[i] = std::max(max_requirements[i], costs[j][i]);
            }
        }
        threshold = max_requirements;
        threshold[Resource::Geode] = 100;
    }

    void step(){
        for (int i = 0; i < 4; ++i){
            resources[i] += robots[i];
        }
    }
    void step_back(){
        for (int i = 0; i < 4; ++i){
            resources[i] -= robots[i];
        }
    }

    [[nodiscard]]
    bool valid(Resource r_type) const {
        if (r_type == Resource::None){
            return true;
        }
        if (threshold[r_type] <= 0){
            return false;
        }
        for (int i = 0; i < 3; ++i){
             if (costs[r_type][i] > resources[i]){
                 return false;
             }
        }
        return true;
    }

    void create(Resource r_type) {
        if (r_type == Resource::None){
            return;
        }
        for (int i = 0; i < 3; ++i){
            resources[i] -= costs[r_type][i];
        }
        robots[r_type] += 1;
        threshold[r_type] -= 1;
    }

    void revert(Resource r_type) {
        if (r_type == Resource::None){
            return;
        }
        for (int i = 0; i < 3; ++i){
            resources[i] += costs[r_type][i];
        }
        robots[r_type] -= 1;
        threshold[r_type] += 1;
    }

    int_t id = 0;
    std::array<int_t, 4> robots {1, 0, 0, 0};
    std::array<int_t, 4> resources {0, 0, 0, 0};
    std::array<std::array<int_t, 4>, 4> costs {};
    std::array<int_t, 4> max_requirements {0, 0, 0, 0};
    std::array<int_t, 4> threshold {0, 0, 0, 0};
};


int_t evaluate(Blueprint& b, int_t steps, int_t current_best){
    if (steps == 0){
        return b.resources[Resource::Geode];
    }

    int_t max_possible = b.resources[Resource::Geode] + b.robots[Resource::Geode] * steps + steps * steps / 2;
    if (max_possible < current_best){
        return current_best;
    }

    int_t best = current_best;
    for (int i = 3; i >= -1; --i){
        auto res = Resource(i);

        if (b.valid(res)){
            b.step();
            b.create(res);

            auto result = evaluate(b, steps - 1, best);
            best = std::max(best, result);

            b.revert(res);
            b.step_back();
        }
    }

    return best;
}

void task_01(std::vector<Blueprint>& blueprints){
    size_t result = 0;

    for (auto& b : blueprints){
        size_t score = evaluate(b, 24, 0);
        result += score * b.id;
    }

    print_solution(19, true, result);
}

void task_02(std::vector<Blueprint>& blueprints){
    size_t result = 1;

    for (int i = 0; i < 3; ++i){
        auto& b = blueprints[i];
        size_t score = evaluate(b, 32, 0);
        result *= score;
    }

    print_solution(19, false, result);
}

void solution(){
    auto data = loadLines(sourceDirectory + "/input");
    std::vector<Blueprint> blueprints;
    blueprints.reserve(data.size());
    for (auto& line : data){
        blueprints.emplace_back(line);
    }

    task_01(blueprints);
    task_02(blueprints);
}

#endif //AOC_19_H