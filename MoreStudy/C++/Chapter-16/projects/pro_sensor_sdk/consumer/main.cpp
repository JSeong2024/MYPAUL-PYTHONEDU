#include <sensor_sdk/statistics.hpp>
#include <array>
#include <iostream>
int main() {
    const std::array samples{4, 8, 12};
    const auto result = sensor_sdk::analyze(samples);
    std::cout << "Consumer avg: " << result.average << '\n';
}
