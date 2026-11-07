#pragma once

#include <algorithm>
#include <cmath>
#include <concepts>
#include <cstddef>
#include <limits>
#include <optional>
#include <ranges>
#include <string>
#include <string_view>
#include <type_traits>
#include <vector>

namespace telemetry {

struct Reading {
    std::string device;
    double value{};
    bool valid{};
};

struct Summary {
    std::size_t count{};
    double minimum{};
    double maximum{};
    double average{};
};

template <typename T>
concept ReadingLike = requires(const T& item) {
    { item.device } -> std::convertible_to<std::string_view>;
    { item.value } -> std::convertible_to<double>;
    { item.valid } -> std::convertible_to<bool>;
};

template <std::ranges::input_range R>
    requires ReadingLike<std::remove_cvref_t<std::ranges::range_reference_t<R>>>
[[nodiscard]] std::optional<Summary> summarize(R&& values) {
    std::size_t count{};
    long double sum{};
    double minimum{};
    double maximum{};
    for (const auto& record : values) {
        const double value = static_cast<double>(record.value);
        if (!static_cast<bool>(record.valid) || !std::isfinite(value)) continue;
        if (count == 0) { minimum = value; maximum = value; }
        else { minimum = std::min(minimum, value); maximum = std::max(maximum, value); }
        sum += value;
        ++count;
    }
    if (count == 0) return std::nullopt;
    return Summary{count, minimum, maximum, static_cast<double>(sum / count)};
}

void print_report(const std::vector<Reading>& readings);

} // namespace telemetry
