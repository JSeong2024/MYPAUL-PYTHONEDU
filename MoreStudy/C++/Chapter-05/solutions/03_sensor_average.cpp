#include <array>
#include <cmath>
#include <optional>
#include <print>

[[nodiscard]] std::optional<double>
average_reading(const std::array<double, 5>& readings) noexcept {
    double sum{};
    for (const double value : readings) {
        if (!std::isfinite(value) || value < 0.0 || value > 100.0) {
            return std::nullopt;
        }
        sum += value;
    }
    return sum / readings.size();
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
