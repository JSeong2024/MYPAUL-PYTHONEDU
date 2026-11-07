cmake_minimum_required(VERSION 3.25)
project(telemetry_pipeline LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(telemetry STATIC src/report.cpp)
target_include_directories(telemetry PUBLIC include)

add_executable(telemetry_demo src/main.cpp)
target_link_libraries(telemetry_demo PRIVATE telemetry)

add_executable(telemetry_tests tests/test_pipeline.cpp)
target_link_libraries(telemetry_tests PRIVATE telemetry)
enable_testing()
add_test(NAME telemetry_tests COMMAND telemetry_tests)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    foreach(target telemetry telemetry_demo telemetry_tests)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
elseif(MSVC)
    foreach(target telemetry telemetry_demo telemetry_tests)
        target_compile_options(${target} PRIVATE /W4 /WX /permissive-)
    endforeach()
endif()
