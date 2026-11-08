#include <array>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>

[[nodiscard]] std::optional<double> average(std::span<const int> samples) {
    // TODO: return nullopt if empty, otherwise calculate the average.
    (void)samples;
    return std::nullopt;
}

int main() {
    const std::array readings{10, 20, 30, 40};
    const auto result = average(readings);
    if (result) {
        std::cout << std::fixed << std::setprecision(1)
                  << "Average: " << *result << '\n';
    }
    std::cout << std::boolalpha;
    std::cout << "Empty: " << !average(std::span<const int>{}) << '\n';
}
