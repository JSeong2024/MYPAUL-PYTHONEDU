#pragma once

#include <cmath>
#include <concepts>
#include <cstddef>
#include <optional>
#include <ranges>
#include <type_traits>

namespace telemetry {

template <typename T>
concept ReadingLike = requires(const T& reading) {
    { reading.value() } -> std::convertible_to<double>;
    { reading.valid() } -> std::convertible_to<bool>;
};

struct Summary {
    std::size_t count{};
    double minimum{};
    double maximum{};
    double average{};
};

template <std::ranges::input_range R>
    requires ReadingLike<std::remove_cvref_t<std::ranges::range_reference_t<R>>>
[[nodiscard]] std::optional<Summary> summarize(R&& readings) {
    Summary result{};
    for (const auto& reading : readings) {
        if (!reading.valid()) continue;
        const double value = static_cast<double>(reading.value());
        if (!std::isfinite(value)) continue;
        if (result.count == 0) {
            result.minimum = value;
            result.maximum = value;
            result.average = value;
        } else {
            if (value < result.minimum) result.minimum = value;
            if (value > result.maximum) result.maximum = value;
            // 누적합의 오버플로를 피하는 점진적 평균. 극단적인 부동소수점
            // 범위는 별도 수치 안정성 정책이 필요하며 여기서는 센서 범위를 가정합니다.
            result.average += (value - result.average) /
                              static_cast<double>(result.count + 1);
        }
        ++result.count;
    }
    if (result.count == 0) return std::nullopt;
    return result;
}
} // namespace telemetry
