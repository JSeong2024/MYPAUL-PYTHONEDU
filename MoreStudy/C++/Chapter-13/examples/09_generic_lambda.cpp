#include <algorithm>
#include <array>
#include <print>

int main() {
    const std::array readings{42, 75, 63, 18};
    const int limit{60};

    const auto above = [limit](const auto& value) {
        return value >= limit;
    };
    const auto count = std::ranges::count_if(readings, above);
    std::println("High readings: {}", count);
}
