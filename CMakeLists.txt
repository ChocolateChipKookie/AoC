cmake_minimum_required(VERSION 3.17)
project(AoC)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE Release)
#set(CMAKE_BUILD_TYPE Debug)

add_executable(AoC
        main.cpp
        util.h
        AoC2020/solutions/01/solution.h
        AoC2020/solutions/02/solution.h
        )