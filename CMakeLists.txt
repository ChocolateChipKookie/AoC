cmake_minimum_required(VERSION 3.17)
project(AoC)

set(CMAKE_CXX_STANDARD 20)

include_directories(../kki_util/include)

add_executable(AoC
        main.cpp
        AoC2020/util.h AoC2019/util.h AoC2018/util.h util/string.h util/array.h)