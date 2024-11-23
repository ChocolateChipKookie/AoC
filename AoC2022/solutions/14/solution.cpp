// Advent of Code 2022 day 14
#ifndef AOC_14_H
#define AOC_14_H
#include "util.hpp"
#include <array>
#include <charconv>
#include <unordered_set>

using int64 = long long;
using Position = std::array<int64, 2>;
template <> struct std::hash<Position> {
  auto operator()(const Position &pos) const -> size_t {
    return pos[0] ^ (pos[0] + pos[1]);
  }
};

std::string sourceDirectory = "../AoC2022/solutions/14";

void task_01(std::unordered_set<Position> blocks) {
  int64 max_y = 0;
  std::unordered_set<Position> sand;

  for (auto &block : blocks) {
    max_y = std::max(block[1], max_y);
  }

  std::array<Position, 3> steps{
      Position{0, 1},
      Position{-1, 1},
      Position{1, 1},
  };

  while (true) {
    Position current = {500, 0};

    while (current[1] < max_y) {
      bool changed = false;
      for (auto &step : steps) {
        Position npos{current[0] + step[0], current[1] + step[1]};
        if (!blocks.contains(npos)) {
          current = npos;
          changed = true;
          break;
        }
      }
      if (!changed) {
        sand.insert(current);
        blocks.insert(current);
        break;
      }
    }
    if (current[1] >= max_y) {
      break;
    }
  }

  print_solution(14, true, sand.size());
}

void task_02(std::unordered_set<Position> blocks) {
  auto data = loadTokens<std::string>(sourceDirectory + "/input");
  std::unordered_set<Position> sand;

  int64 max_y = 0;
  for (auto &block : blocks) {
    max_y = std::max(block[1], max_y);
  }
  for (int64 i = 500 - max_y; i <= 500 + max_y; ++i) {
    blocks.insert({i, max_y});
  }

  std::array<Position, 3> steps{
      Position{0, 1},
      Position{-1, 1},
      Position{1, 1},
  };

  Position source = {500, 0};
  while (!sand.contains(source)) {
    Position current = source;

    while (true) {
      bool changed = false;
      for (auto &step : steps) {
        Position npos{current[0] + step[0], current[1] + step[1]};
        if (!blocks.contains(npos)) {
          current = npos;
          changed = true;
          break;
        }
      }
      if (!changed) {
        sand.insert(current);
        blocks.insert(current);
        break;
      }
    }
  }

  print_solution(14, false, sand.size());
}

int main() {
  auto data = loadLines(sourceDirectory + "/input");
  std::unordered_set<Position> blocks;

  auto parse_position = [](const kki::string &position) -> Position {
    auto tokens = position.split(',');
    int64 x, y;
    std::from_chars(tokens[0].begin(), tokens[0].end(), x);
    std::from_chars(tokens[1].begin(), tokens[1].end(), y);
    return {x, y};
  };

  for (auto &line : data) {
    auto tokens = line.split(" -> ");
    Position current = parse_position(tokens[0]);
    for (size_t i = 1; i < tokens.size(); ++i) {
      Position next = parse_position(tokens[i]);
      int64 length =
          std::abs(next[0] - current[0]) + std::abs(next[1] - current[1]);
      Position direction = {(next[0] - current[0]) / length,
                            (next[1] - current[1]) / length};
      for (int d = 0; d < length; ++d) {
        blocks.insert(
            {current[0] + direction[0] * d, current[1] + direction[1] * d});
      }
      current = next;
    }
    blocks.insert(current);
  }

  task_01(blocks);
  task_02(blocks);
}

#endif // AOC_14_H
