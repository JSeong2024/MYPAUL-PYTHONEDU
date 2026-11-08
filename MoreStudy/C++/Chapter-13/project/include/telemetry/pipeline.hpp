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
    // TODO 1: 입력 Range를 순회하며 유효한 측정값만 선택합니다.
    // TODO 2: 유한한 측정값의 최소·최대·평균·건수를 계산합니다.
    // TODO 3: 유효 데이터가 없으면 std::nullopt를 반환합니다.
    // 임시 반환문: 학생이 구현하면 제거하세요.
    (void)readings;
    return std::nullopt;
}
} // namespace telemetry
