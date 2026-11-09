#include "sensor/analyzer.hpp"

#include <chrono>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string_view>
#include <vector>

namespace {
[[nodiscard]] std::vector<sensor::Reading> build_data(std::size_t count) {
    std::vector<sensor::Reading> readings;
    readings.reserve(count);
    for (std::size_t index = 0; index < count; ++index) {
        const int device = static_cast<int>(index % 2048 + 1);
        const int value = static_cast<int>(index % 101);
        readings.push_back({device, value});
    }
    return readings;
}
} // namespace

int main(int argc, char* argv[]) {
    if (argc == 1) {
        const std::vector<sensor::Reading> sample{
            {1, 20}, {2, 35}, {1, 30}, {-1, 40}, {2, 101}, {3, 10}, {3, 30}};
        const auto baseline = sensor::analyze_reference(sample);
        const auto optimized = sensor::analyze_optimized(sample);
        std::cout << "Devices: " << optimized.devices.size() << '\n';
        std::cout << "Accepted: " << optimized.accepted
                  << ", Rejected: " << optimized.rejected << '\n';
        std::cout << "Total: " << optimized.total << '\n';
        std::cout << std::boolalpha << "Matches: " << (baseline == optimized) << '\n';
        return baseline == optimized ? 0 : 1;
    }
    if (argc != 3 || std::string_view{argv[1]} != "--benchmark") {
        std::cerr << "Usage: sensor_batch_analyzer [--benchmark <count>]\n";
        return 2;
    }
    char* end = nullptr;
    const unsigned long long parsed = std::strtoull(argv[2], &end, 10);
    if (end == argv[2] || *end != '\0' || argv[2][0] == '-' || parsed == 0 ||
        parsed > 1000000ULL) {
        std::cerr << "Invalid count (1..1000000)\n";
        return 2;
    }
    const auto readings = build_data(static_cast<std::size_t>(parsed));
    using Clock = std::chrono::steady_clock;
    const auto start_ref = Clock::now();
    const auto baseline = sensor::analyze_reference(readings);
    const auto end_ref = Clock::now();
    const auto optimized = sensor::analyze_optimized(readings);
    const auto end_opt = Clock::now();
    const auto to_milliseconds = [](auto interval) {
        return std::chrono::duration<double, std::milli>(interval).count();
    };
    std::cout << "Rows: " << readings.size() << '\n';
    std::cout << "Baseline ms: " << to_milliseconds(end_ref - start_ref) << '\n';
    std::cout << "Optimized ms: " << to_milliseconds(end_opt - end_ref) << '\n';
    std::cout << std::boolalpha << "Matches: " << (baseline == optimized) << '\n';
    return baseline == optimized ? 0 : 1;
}
