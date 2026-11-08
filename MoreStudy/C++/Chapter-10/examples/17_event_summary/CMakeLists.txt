cmake_minimum_required(VERSION 3.20)
project(event_summary LANGUAGES CXX)

add_library(event_summary_lib summary.cpp)
target_compile_features(event_summary_lib PUBLIC cxx_std_20)
target_include_directories(event_summary_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(event_summary main.cpp)
target_link_libraries(event_summary PRIVATE event_summary_lib)

add_executable(event_summary_tests summary_tests.cpp)
target_link_libraries(event_summary_tests PRIVATE event_summary_lib)

foreach(target event_summary_lib event_summary event_summary_tests)
    if(MSVC)
        target_compile_options(${target} PRIVATE /W4 /EHsc /utf-8)
    else()
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endforeach()

enable_testing()
add_test(NAME summary_logic COMMAND event_summary_tests)
add_test(NAME report_output COMMAND event_summary)
set_tests_properties(report_output PROPERTIES
    PASS_REGULAR_EXPRESSION "Total: 5"
)
