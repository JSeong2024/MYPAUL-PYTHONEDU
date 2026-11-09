#include "sensor_sdk/statistics.hpp"
#include <algorithm>
#include <stdexcept>
namespace sensor_sdk {
Statistics analyze(std::span<const int> samples) {
    if (samples.empty()) throw std::invalid_argument("no samples");
    Statistics result{samples.size(), samples.front(), samples.front(), 0.0};
    long long sum{};
    for (const int value : samples) {
        if (value < 0 || value > 1000) throw std::invalid_argument("sample out of range");
        result.minimum = std::min(result.minimum, value);
        result.maximum = std::max(result.maximum, value);
        sum += value; // 개수의 한계도 운영 환경에서는 별도 고려
    }
    result.average = static_cast<double>(sum) / static_cast<double>(samples.size());
    return result;
}
}
