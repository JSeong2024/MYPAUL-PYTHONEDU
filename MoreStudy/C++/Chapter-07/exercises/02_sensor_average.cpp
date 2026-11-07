#include <array>
#include <optional>
#include <print>
#include <span>

// 문제: 빈 구간은 nullopt, 그 외에는 평균 반환.
// 정수 합산 오버플로를 피하기 위해 double로 누적.
[[nodiscard]] std::optional<double> average(std::span<const int> samples) {
    // TODO: 빈 구간 검사 / 누적 / 평균 반환
    (void)samples;
    return std::nullopt;
}

int main() {
    const std::array readings{10, 20, 30, 40};
    if (const auto value = average(readings)) {
        std::println("Average: {:.1f}", *value);
    }
    const std::span<const int> empty{};
    std::println("Empty: {}", !average(empty));
}
