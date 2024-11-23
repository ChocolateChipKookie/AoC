#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include "array.hpp"
#include "string.hpp"
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

template <typename T_token>
std::vector<T_token> loadTokens(const std::string &filepath) {
  std::ifstream ifs(filepath);
  std::istream_iterator<T_token> begin(ifs), end;
  std::vector<T_token> inputs{begin, end};
  ifs.close();
  return inputs;
}

std::vector<kki::string> loadLines(const std::string &filepath,
                                   bool include_empty = true) {
  std::ifstream ifs(filepath);
  std::string line;
  std::vector<kki::string> inputs;
  while (std::getline(ifs, line)) {
    if (include_empty || !line.empty()) {
      inputs.emplace_back(line.c_str());
    }
  }
  return inputs;
}

template <class T_data> Grid<T_data> loadGrid(const std::string &filepath) {
  std::ifstream ifs(filepath);
  Grid<T_data> g;
  ifs >> g;
  return g;
}

template <typename T_res>
void print_solution(size_t day, bool easy, const T_res &result,
                    const std::string &result_message = "") {
  std::cout << "Day: " << day << "\nDifficulty: " << (easy ? "Easy" : "Hard")
            << "\nResult: ";
  if (!result_message.empty()) {
    std::cout << result_message;
  }
  std::cout << result << std::endl;
}

#endif // AOC_UTIL_H
