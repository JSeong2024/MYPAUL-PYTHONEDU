#include <cmath>
#include <iostream>
#include <print>

[[nodiscard]] double to_fahrenheit(double celsius) noexcept {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    double celsius{};
    std::cout << "Celsius: " << std::flush;
    if (!(std::cin >> celsius) || !std::isfinite(celsius)) {
        std::println("Invalid temperature");
        return 1;
    }

    std::println("Fahrenheit: {:.1f}", to_fahrenheit(celsius));
}
