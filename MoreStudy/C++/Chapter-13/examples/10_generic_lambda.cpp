#include <algorithm>
#include <array>
#include <print>

int main() {
    const std::array readings{14, 30, 27, 42};
    const int threshold{28};
    const auto count = std::ranges::count_if(readings, [threshold](const auto& value) {
        return value >= threshold;
    });
    std::println("Alerts: {}", count);
}
