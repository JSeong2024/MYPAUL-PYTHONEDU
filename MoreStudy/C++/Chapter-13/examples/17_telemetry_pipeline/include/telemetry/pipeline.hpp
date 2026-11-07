#pragma once

#include <cmath>
#include <concepts>
#include <cstddef>
#include <optional>
#include <ranges>
#include <type_traits>

namespace telemetry {

template <typename T>
concept ReadingLike = requires(const T& r) {
    { r.value() } -> std::convertible_to<double>;
    { r.valid() } -> std::convertible_to<bool>;
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
    double sum{};

    for (const auto& reading : readings) {
        if (!reading.valid()) continue;
        const double value = static_cast<double>(reading.value());
        if (!std::isfinite(value)) continue;

        if (result.count == 0) {
            result.minimum = value;
            result.maximum = value;
        } else {
            if (value < result.minimum) result.minimum = value;
            if (value > result.maximum) result.maximum = value;
        }
        ++result.count;
        sum += value;
    }
    if (result.count == 0) return std::nullopt;
    result.average = sum / static_cast<double>(result.count);
    return result;
}

} // namespace telemetry
