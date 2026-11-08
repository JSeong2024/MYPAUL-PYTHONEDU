#include <array>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>
#include <vector>

[[nodiscard]] std::optional<double> average(std::span<const int> values) {
    if (values.empty()) {
        return std::nullopt;
    }
    double total{};
    for (const int value : values) {
        total += value;
    }
    return total / static_cast<double>(values.size());
}

int main() {
    const std::array fixed{10, 20, 30};
    const std::vector dynamic{40, 50, 60};
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Fixed: " << *average(fixed) << '\n';
    std::cout << "Dynamic: " << *average(dynamic) << '\n';
    std::cout << std::boolalpha;
    std::cout << "Empty: " << !average(std::span<const int>{}) << '\n';
}
