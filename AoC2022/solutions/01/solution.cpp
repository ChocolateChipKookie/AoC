// Advent of Code 2022 day 1
#ifndef AOC_01_H
#define AOC_01_H
#include "util.hpp"
#include <algorithm>
#include <numeric>
#include <queue>

std::string sourceDirectory = "../AoC2022/solutions/01";

std::vector<std::vector<size_t>> get_groups() {
  auto data = loadLines(sourceDirectory + "/input", true);
  std::vector<std::vector<size_t>> groups;
  groups.reserve(100);
  for (auto &line : data) {
    if (line.size() == 0 || groups.empty()) {
      groups.emplace_back();
      continue;
    }
    groups.back().push_back(std::stoi(line.cstr()));
  }
  return groups;
}

void task_01() {
  auto groups = get_groups();
  std::vector<size_t> sums;
  sums.reserve(groups.size());
  for (auto &group : groups) {
    sums.push_back(std::accumulate(group.begin(), group.end(), 0ull));
  }
  auto max = std::max_element(sums.begin(), sums.end());
  print_solution(1, true, *max);
}

void task_02() {
  std::priority_queue<size_t, std::vector<size_t>, std::greater<>> pqueue;
  for (auto &group : get_groups()) {
    size_t sum = std::accumulate(group.begin(), group.end(), 0ull);
    pqueue.push(sum);
    if (pqueue.size() > 3) {
      pqueue.pop();
    }
  }
  size_t sum = 0;
  while (!pqueue.empty()) {
    sum += pqueue.top();
    pqueue.pop();
  }
  print_solution(1, false, sum);
}

int main() {
  task_01();
  task_02();
}

#endif // AOC_01_H
