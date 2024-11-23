// Advent of Code 2022 day 15
#ifndef AOC_15_H
#define AOC_15_H
#include "util.hpp"
#include <algorithm>
#include <charconv>
#include <limits>

std::string sourceDirectory = "../AoC2022/solutions/15";

using int_t = long long;
struct Beacon {
  int_t x, y;
};

struct Sensor {
  int_t x, y;
  Beacon beacon;
};

int_t sweep(std::vector<std::array<int_t, 2>> &ranges) {
  std::sort(ranges.begin(), ranges.end(),
            [](const auto &r1, const auto &r2) { return r1[0] < r2[0]; });
  int_t occupied = 0;
  int_t current_x = std::numeric_limits<int_t>::min();

  for (auto &range : ranges) {
    if (range[1] > current_x) {
      int_t start = std::max(current_x, range[0]);
      occupied += range[1] - start;
      current_x = range[1];
    }
  }
  return occupied;
}

void create_ranges(std::vector<Sensor> &sensors,
                   std::vector<std::array<int_t, 2>> &container, int_t y,
                   int_t x_start, int_t x_end) {
  container.clear();

  for (auto &sensor : sensors) {
    auto &beacon = sensor.beacon;
    int_t bs_distance =
        std::abs(sensor.x - beacon.x) + std::abs(sensor.y - beacon.y);
    int_t y_distance = std::abs(sensor.y - y);
    int_t width = bs_distance - y_distance;

    int_t min_x = std::max(std::min(sensor.x - width, x_end), x_start);
    int_t max_x = std::max(std::min(sensor.x + width, x_end), x_start);

    if (width > 0 && min_x != max_x) {
      container.push_back({min_x, max_x});
    }
  }
}

void task_01(std::vector<Sensor> &sensors, int_t y) {
  std::vector<std::array<int_t, 2>> ranges;
  create_ranges(sensors, ranges, y, std::numeric_limits<int_t>::min(),
                std::numeric_limits<int_t>::max());
  print_solution(15, true, sweep(ranges));
}

void task_02(std::vector<Sensor> &sensors) {
  std::vector<std::array<int_t, 2>> ranges;
  const int_t max = 4000000;
  for (int_t y = 0; y <= max; ++y) {
    create_ranges(sensors, ranges, y, 0, max);
    int_t occupied = sweep(ranges);
    if (occupied < max) {
      int_t x = 0;
      for (auto &range : ranges) {
        if (range[0] <= x && x <= range[1]) {
          x = range[1] + 1;
        }
        if (x < range[0]) {
          int_t result = x * max + y;
          print_solution(15, false, result);
          return;
        }
      }
    }
  }
}

int main() {
  auto data = loadLines(sourceDirectory + "/input");
  std::vector<Sensor> sensors;
  sensors.reserve(data.size());

  auto parse = [](const kki::string &str) {
    int_t result;
    std::from_chars(str.begin(), str.end(), result);
    return result;
  };

  for (auto &line : data) {
    auto x_sensor_s = line.find('=') + 1;
    auto x_sensor_e = line.find(',', x_sensor_s);

    auto y_sensor_s = line.find('=', x_sensor_e) + 1;
    auto y_sensor_e = line.find(':', y_sensor_s);

    auto x_beacon_s = line.find('=', y_sensor_e) + 1;
    auto x_beacon_e = line.find(',', x_beacon_s);

    auto y_beacon_s = line.find('=', x_beacon_e) + 1;

    sensors.push_back(
        Sensor{.x = parse(line.substr(x_sensor_s, x_sensor_e)),
               .y = parse(line.substr(y_sensor_s, y_sensor_e)),
               .beacon = Beacon{.x = parse(line.substr(x_beacon_s, x_beacon_e)),
                                .y = parse(line.substr(y_beacon_s))}});
  }

  task_01(sensors, 2000000);
  task_02(sensors);
}

#endif // AOC_15_H
