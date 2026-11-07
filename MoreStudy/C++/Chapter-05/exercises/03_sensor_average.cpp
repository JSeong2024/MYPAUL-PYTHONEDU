#include <array>
#include <cmath>
#include <optional>
#include <print>

[[nodiscard]] std::optional<double>
average_reading(const std::array<double, 5>& readings) noexcept {
    // TODO: 모든 값이 유한하고 0~100 범위인지 확인
    // TODO: 유효하지 않은 샘플이 있으면 std::nullopt 반환
    // TODO: 전체 평균을 계산하여 반환
    (void)readings;
    return std::nullopt;
}

int main() {
    constexpr std::array readings{12.0, 14.0, 13.0, 11.0, 15.0};
    const auto average = average_reading(readings);
    if (!average) {
        std::println("Invalid sensor data");
        return 1;
    }
    std::println("Average: {:.1f}", *average);
}
