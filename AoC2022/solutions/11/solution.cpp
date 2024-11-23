// Advent of Code 2022 day 11
#ifndef AOC_11_H
#define AOC_11_H
#include "util.hpp"
#include <algorithm>
#include <charconv>

std::string sourceDirectory = "../AoC2022/solutions/11";

struct Monkey {
  using T_int = uint64_t;
  T_int inspections = 0;
  std::vector<T_int> items;
  std::function<T_int(T_int)> operation;
  std::function<T_int(T_int)> test;
  T_int divisor{};
  T_int if_true{};
  T_int if_false{};
};

Monkey::T_int run(std::vector<Monkey> monkeys, int total_rounds,
                  bool level_drop) {
  Monkey::T_int divisor = 1;
  for (auto &monkey : monkeys) {
    divisor *= monkey.divisor;
  }

  for (int round = 0; round < total_rounds; ++round) {
    for (auto &monkey : monkeys) {
      for (auto item : monkey.items) {
        auto worry_level = monkey.operation(item) % divisor;
        monkey.inspections += 1;
        if (level_drop) {
          worry_level /= 3;
        }
        auto next = monkey.test(worry_level) ? monkey.if_true : monkey.if_false;
        monkeys[next].items.push_back(worry_level);
      }
      monkey.items.clear();
    }
  }
  std::sort(monkeys.begin(), monkeys.end(),
            [](const Monkey &m1, const Monkey &m2) {
              return m1.inspections > m2.inspections;
            });
  return monkeys[0].inspections * monkeys[1].inspections;
}

int main() {
  auto data = loadLines(sourceDirectory + "/input");
  std::vector<Monkey> monkeys;
  monkeys.reserve(data.size() / 7);

  auto fetch_last_int = [](const kki::string &val) {
    auto tokens = val.split(" ");
    Monkey::T_int div;
    std::from_chars(tokens.back().begin(), tokens.back().end(), div, 10);
    return div;
  };

  for (int i = 0; i < data.size();) {
    auto &header = data[i++];
    auto &items = data[i++];
    auto &operation = data[i++];
    auto &test = data[i++];
    auto &if_true = data[i++];
    auto &if_false = data[i++];
    i++; // Blank line

    auto tokens = items.split(": ");
    tokens = tokens[1].split(", ");

    Monkey m;
    for (const auto &token : tokens) {
      Monkey::T_int value;
      std::from_chars(token.begin(), token.end(), value, 10);
      m.items.push_back(value);
    }
    Monkey::T_int div = fetch_last_int(test);
    m.divisor = div;
    m.test = [div](Monkey::T_int value) -> bool { return value % div == 0; };
    m.if_true = fetch_last_int(if_true);
    m.if_false = fetch_last_int(if_false);

    operation = operation.split(" = ")[1];
    auto op_tokens = operation.split();
    auto func =
        op_tokens[1][0] == '*'
            ? [](Monkey::T_int i1, Monkey::T_int i2) { return i1 * i2; }
            : [](Monkey::T_int i1, Monkey::T_int i2) { return i1 + i2; };

    if (op_tokens[2] == "old") {
      m.operation = [func](Monkey::T_int old) { return func(old, old); };
    } else {
      Monkey::T_int second;
      std::from_chars(op_tokens[2].begin(), op_tokens[2].end(), second, 10);
      m.operation = [func, second](Monkey::T_int old) {
        return func(old, second);
      };
    }

    monkeys.push_back(std::move(m));
  }

  print_solution(11, true, run(monkeys, 20, true));
  print_solution(11, false, run(monkeys, 10000, false));
}

#endif // AOC_11_H
