#include <array>
#include <iostream>
#include <span>
#include <vector>

[[nodiscard]] int sum_readings(std::span<const int> readings) {
    int total{};
    for (const int value : readings) total += value;
    return total;
}

int main() {
    const std::array<int, 3> fixed{10, 20, 30};
    const std::vector<int> dynamic{4, 6};
    std::cout << "Array total: " << sum_readings(fixed) << '\n';
    std::cout << "Vector total: " << sum_readings(dynamic) << '\n';
}
