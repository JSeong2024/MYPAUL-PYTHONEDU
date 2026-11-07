#include <algorithm>
#include <array>
#include <print>

int main() {
    constexpr std::array<int, 5> readings{21, 24, 19, 23, 22};
    const auto [minimum, maximum] = std::ranges::minmax(readings);

    std::println("Samples: {}", readings.size());
    std::println("Minimum: {} C", minimum);
    std::println("Maximum: {} C", maximum);
}
