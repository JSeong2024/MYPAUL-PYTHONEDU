#include "sensor_sdk/statistics.hpp"
#include <stdexcept>
namespace sensor_sdk {
Statistics analyze(std::span<const int> samples) {
    // TODO: 빈 입력과 0~1000 범위 검사, min/max/mean 계산.
    (void)samples;
    return {};
}
}
