#pragma once
#include <cstddef>
#include <span>
namespace sensor_sdk {
struct Statistics {
    std::size_t count{};
    int minimum{};
    int maximum{};
    double average{};
};
[[nodiscard]] Statistics analyze(std::span<const int> samples);
}
