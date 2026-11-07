#include <algorithm>
#include <array>
#include <print>

int main() {
    constexpr std::array readings{42, 68, 73, 49, 81, 55};
    const int threshold{60};

    const auto is_high = [threshold](int value) {
        return value > threshold;
    };

    const auto count = std::ranges::count_if(readings, is_high);
    std::println("Above threshold: {}", count);
}
