cmake_minimum_required(VERSION 3.17)
project(AoC)

set(CMAKE_CXX_STANDARD 23)

include_directories(AoC2018, AoC2019, AoC2020, AoC2021, AoC2022, AoC2023)

add_executable(AoC
  main.cpp
  AoC2023/solutions/12/solution.h
  AoC2023/util.h
  AoC2022/util.h
  AoC2021/util.h
  AoC2020/util.h
  AoC2019/util.h
  AoC2018/util.h
  util/string.h
  util/array.h)
