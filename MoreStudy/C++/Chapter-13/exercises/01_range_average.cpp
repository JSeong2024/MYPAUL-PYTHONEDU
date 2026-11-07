#include <concepts>
#include <optional>
#include <print>
#include <ranges>
#include <vector>

// TODO: 정수·실수 Range를 입력받아 평균을 계산
// 조건: 빈 Range에서는 std::nullopt, 유효한 Range에서는 double 평균 반환
// std::ranges::input_range 및 타입 제약 적용

template <std::ranges::input_range R>
    requires std::convertible_to<std::ranges::range_reference_t<R>, double>
[[nodiscard]] std::optional<double> mean(R&& values) {
    // TODO: 누적 및 개수 계산
    (void)values;
    return std::nullopt;
}

int main() {
    const std::vector values{10, 20, 30};
    if (const auto result = mean(values)) std::println("Mean: {:.1f}", *result);
}
