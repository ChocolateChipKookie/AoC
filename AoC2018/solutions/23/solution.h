//Advent of Code 2018 day 23
#ifndef AOC_23_H
#define AOC_23_H
#include "../../util.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <array>

std::string sourceDirectory = "../AoC2018/solutions/23";

using int_t = long long;
using Position = std::array<int_t, 3>;

int_t distance(const Position& p1, const Position& p2){
    return  std::abs(p1[0] - p2[0]) +
            std::abs(p1[1] - p2[1]) +
            std::abs(p1[2] - p2[2]);
}

struct Nanobot {
    Position pos {};
    int_t radius {};
};

struct Intersection{
    explicit Intersection () = default;
    explicit Intersection (const Nanobot& nano) {
        cluster.push_back(&nano);
    }

    std::vector<const Nanobot*> cluster;

    bool intersects(const Nanobot& nano){
        auto predicate = [&nano](const Nanobot* n){
            return distance(nano.pos, n->pos) < (nano.radius + n->radius);
        };
        return std::all_of(cluster.begin(), cluster.end(), predicate);
    }
};


void task_01(std::vector<Nanobot>& bots){
    auto data = loadTokens<std::string>(sourceDirectory + "/input");
    size_t res = 0;

    print_solution(23, true, res);
}


void task_02(std::vector<Nanobot>& bots){

    Intersection best_cluster;
    int_t best_score = 0;

    for (auto& boss : bots){
        Intersection cluster(boss);
        for (auto& bot : bots){
            if (cluster.intersects(bot)){
                cluster.cluster.push_back(&bot);
            }
        }
        if (cluster.cluster.size() > best_score){
            best_score = cluster.cluster.size();
            best_cluster = cluster;
            if (best_score > 500){
                break;
            }
        }
    }

    Nanobot center {{0, 0, 0}, 0};
    int_t lo = 0;
    int_t hi = std::numeric_limits<int_t>::max();
    while (hi > lo){
        auto mid = (hi + lo) / 2;
        center.radius = mid;
        if (best_cluster.intersects(center)){
            hi = mid;
        }
        else {
            lo = mid + 1;
        }
    }

    print_solution(23, false, lo);
}

void solution(){
    auto data = loadLines<kki::string>(sourceDirectory + "/input");

    auto parse_int = [](const kki::string& str) -> int_t {
        int_t result;
        std::from_chars(str.begin(), str.end(), result);
        return result;
    };

    std::vector<Nanobot> bots;
    bots.reserve(data.size());
    for (auto& line : data){
        auto b_open = line.find('<');
        auto b_close = line.find('>');
        auto equal = line.find('=', b_close);
        auto pos_s = line.substr(b_open + 1, b_close);
        auto rad_s = line.substr(equal + 1);
        auto tokens = pos_s.split(',');

        Position pos {
                parse_int(tokens[0]),
                parse_int(tokens[1]),
                parse_int(tokens[2])
        };
        bots.push_back({pos, parse_int(rad_s)});
    }

    task_01(bots);
    task_02(bots);
}

#endif //AOC_23_H