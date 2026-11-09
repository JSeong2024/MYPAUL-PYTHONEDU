#include "sensor/analyzer.hpp"
namespace sensor {
Report analyze_reference(std::span<const Reading> readings) {
    // TODO: 입력 순회 및 기준 정산. 장치 ID별 선형 검색.
    (void)readings;
    return {};
}
Report analyze_optimized(std::span<const Reading> readings) {
    // TODO: std::unordered_map + std::ranges::sort를 이용한 최적화.
    (void)readings;
    return {};
}
} // namespace sensor
