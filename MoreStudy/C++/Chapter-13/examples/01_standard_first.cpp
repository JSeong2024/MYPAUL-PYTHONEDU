#include <algorithm>
#include <array>
#include <print>

int main() {
    std::println("Max: {}", std::max(12, 19));
    std::println("Max double: {}", std::max(1.5, 2.75));
    std::println("Explicit type: {}", std::max<double>(1, 2.5));

    const std::array readings{18, 26, 21, 32, 24};
    const auto highest = std::ranges::max_element(readings);
    std::println("Highest reading: {}", *highest);
}
