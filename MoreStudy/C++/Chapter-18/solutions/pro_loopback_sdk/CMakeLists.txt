cmake_minimum_required(VERSION 3.20)
project(ProLink VERSION 1.0.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
find_package(Threads REQUIRED)
add_library(prolink STATIC src/api.cpp)
add_library(ProLink::prolink ALIAS prolink)
target_compile_features(prolink PUBLIC cxx_std_20)
set_target_properties(prolink PROPERTIES CXX_EXTENSIONS OFF EXPORT_NAME prolink)
target_include_directories(prolink PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_link_libraries(prolink PRIVATE Threads::Threads)
if(WIN32)
  target_link_libraries(prolink PRIVATE ws2_32)
endif()
if(MSVC)
  target_compile_options(prolink PRIVATE /W4 /EHsc /permissive- /utf-8)
else()
  target_compile_options(prolink PRIVATE -Wall -Wextra -Wpedantic)
endif()
add_executable(prolink_demo src/main.cpp)
target_link_libraries(prolink_demo PRIVATE prolink)
include(CTest)
if(BUILD_TESTING)
  add_executable(prolink_tests tests/test_api.cpp)
  target_link_libraries(prolink_tests PRIVATE prolink)
  add_test(NAME prolink_behavior COMMAND prolink_tests)
  add_test(NAME prolink_output COMMAND prolink_demo)
  set_tests_properties(prolink_output PROPERTIES PASS_REGULAR_EXPRESSION "Reply: HELLO")
endif()
install(TARGETS prolink EXPORT ProLinkTargets ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
set(package_dir "${CMAKE_INSTALL_LIBDIR}/cmake/ProLink")
configure_package_config_file(cmake/ProLinkConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/ProLinkConfig.cmake"
  INSTALL_DESTINATION "${package_dir}")
write_basic_package_version_file("${CMAKE_CURRENT_BINARY_DIR}/ProLinkConfigVersion.cmake"
  VERSION ${PROJECT_VERSION} COMPATIBILITY SameMajorVersion)
install(EXPORT ProLinkTargets NAMESPACE ProLink:: DESTINATION "${package_dir}")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/ProLinkConfig.cmake"
              "${CMAKE_CURRENT_BINARY_DIR}/ProLinkConfigVersion.cmake"
        DESTINATION "${package_dir}")
