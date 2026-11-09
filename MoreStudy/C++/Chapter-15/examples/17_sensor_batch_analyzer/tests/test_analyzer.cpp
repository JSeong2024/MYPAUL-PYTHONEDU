#include "sensor/analyzer.hpp"

#include <algorithm>
#include <array>
#include <stdexcept>
#include <vector>

static void check(bool result) {
    if (!result) throw std::runtime_error("sensor analyzer test failed");
}

int main() {
    const std::vector<sensor::Reading> sample{
        {1, 20}, {2, 35}, {1, 30}, {-1, 40}, {2, 101}, {3, 10}, {3, 30}};
    const auto first = sensor::analyze_reference(sample);
    const auto second = sensor::analyze_optimized(sample);
    check(first == second);
    check(second.accepted == 5);
    check(second.rejected == 2);
    check(second.total == 125);
    check((second.devices == std::vector<sensor::DeviceStat>{{1, 2, 50},
                                                              {2, 1, 35}, {3, 2, 40}}));
    const std::array<sensor::Reading, 0> empty{};
    check(sensor::analyze_optimized(empty) == sensor::Report{});
    const std::array invalid{sensor::Reading{0, 9}, sensor::Reading{2, -1}};
    const auto rejected = sensor::analyze_optimized(invalid);
    check(rejected.accepted == 0 && rejected.rejected == 2 && rejected.total == 0);
    const std::array valid_zero{sensor::Reading{2, 0}, sensor::Reading{2, 100}};
    const auto boundaries = sensor::analyze_optimized(valid_zero);
    check(boundaries.accepted == 2 && boundaries.total == 100);
    std::vector<sensor::Reading> large;
    large.reserve(100000);
    for (int i = 0; i < 100000; ++i) {
        large.push_back({i % 64 + 1, i % 101});
    }
    check(sensor::analyze_reference(large) == sensor::analyze_optimized(large));
    // 순서가 다른 입력도 출력 순서는 device_id 기준으로 동일함.
    std::ranges::reverse(large);
    check(sensor::analyze_reference(large) == sensor::analyze_optimized(large));
    // 내부 순서를 바꿔도 동일한 집계가 나온다.
    const auto one = sensor::analyze_optimized(large);
    std::ranges::reverse(large);
    check(sensor::analyze_optimized(large) == one);
}
