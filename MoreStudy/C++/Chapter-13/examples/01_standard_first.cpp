#include <algorithm>
#include <array>
#include <iostream>

int main() {
    std::cout << "Max: " << std::max(12, 19) << '\n';
    std::cout << "Max double: " << std::max(1.5, 2.75) << '\n';
    std::cout << "Explicit type: " << std::max<double>(1, 2.5) << '\n';
    const std::array readings{18, 26, 21, 32, 24};
    const auto highest = std::ranges::max_element(readings);
    if (highest != readings.end()) {
        std::cout << "Highest reading: " << *highest << '\n';
    }
}
