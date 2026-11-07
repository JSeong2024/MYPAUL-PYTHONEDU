cmake_minimum_required(VERSION 3.20)
project(robot_monitor LANGUAGES CXX)

add_executable(robot_monitor main.cpp monitor.cpp)
target_compile_features(robot_monitor PRIVATE cxx_std_23)

if(MSVC)
    target_compile_options(robot_monitor PRIVATE /W4 /utf-8)
else()
    target_compile_options(robot_monitor PRIVATE -Wall -Wextra -Wpedantic)
endif()
