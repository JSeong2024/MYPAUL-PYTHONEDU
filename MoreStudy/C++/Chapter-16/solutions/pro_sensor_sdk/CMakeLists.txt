cmake_minimum_required(VERSION 3.23)
project(SensorSDK VERSION 1.2.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

option(SENSORSDK_BUILD_TESTS "Build SDK tests and example" ON)
add_library(sensor_sdk_core STATIC src/statistics.cpp)
add_library(SensorSDK::core ALIAS sensor_sdk_core)
set_target_properties(sensor_sdk_core PROPERTIES EXPORT_NAME core CXX_EXTENSIONS OFF)
target_compile_features(sensor_sdk_core PUBLIC cxx_std_20)
target_include_directories(sensor_sdk_core PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
if(MSVC)
    target_compile_options(sensor_sdk_core PRIVATE /W4 /EHsc /permissive- /utf-8)
else()
    target_compile_options(sensor_sdk_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(SENSORSDK_BUILD_TESTS)
    enable_testing()
    add_executable(sensor_cli tools/sensor_cli.cpp)
    target_link_libraries(sensor_cli PRIVATE SensorSDK::core)
    add_executable(sensor_tests tests/test_statistics.cpp)
    target_link_libraries(sensor_tests PRIVATE SensorSDK::core)
    add_test(NAME sdk_behavior COMMAND sensor_tests)
    add_test(NAME sdk_cli_output COMMAND sensor_cli)
    set_tests_properties(sdk_cli_output PROPERTIES PASS_REGULAR_EXPRESSION "count=3 min=10 max=30 avg=20")
endif()

install(TARGETS sensor_sdk_core EXPORT SensorSDKTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
set(_sensor_sdk_package_dir ${CMAKE_INSTALL_LIBDIR}/cmake/SensorSDK)
install(EXPORT SensorSDKTargets
    FILE SensorSDKTargets.cmake
    NAMESPACE SensorSDK::
    DESTINATION ${_sensor_sdk_package_dir}
)
configure_package_config_file(
    cmake/SensorSDKConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/SensorSDKConfig.cmake
    INSTALL_DESTINATION ${_sensor_sdk_package_dir}
)
write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/SensorSDKConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/SensorSDKConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/SensorSDKConfigVersion.cmake
    DESTINATION ${_sensor_sdk_package_dir}
)
