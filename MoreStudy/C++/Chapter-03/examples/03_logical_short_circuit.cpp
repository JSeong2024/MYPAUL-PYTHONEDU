#include <iostream>

int main() {
    constexpr int samples{0};
    constexpr int total{150};
    constexpr bool connected{true};
    constexpr double temperature_c{78.5};

    const bool high_average = (samples != 0) && (total / samples > 30);
    const bool alarm = connected && (temperature_c >= 75.0);

    std::cout << std::boolalpha;
    std::cout << "High average: " << high_average << '\n';
    std::cout << "Alarm: " << alarm << '\n';
}
