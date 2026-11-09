#include "sensor_sdk/statistics.hpp"
#include <array>
#include <iostream>
int main() {
    const std::array readings{10, 20, 30};
    const auto result = sensor_sdk::analyze(readings);
    std::cout << "count=" << result.count << " min=" << result.minimum
              << " max=" << result.maximum << " avg=" << result.average << '\n';
}
