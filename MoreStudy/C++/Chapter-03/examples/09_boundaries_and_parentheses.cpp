#include <iostream>

int main() {
    constexpr int battery_percent{20};
    constexpr bool connected{true};
    constexpr double temperature_c{78.0};

    const bool valid_battery{battery_percent >= 0 && battery_percent <= 100};
    const bool warning{connected &&
                       (battery_percent <= 20 || temperature_c >= 75.0)};

    std::cout << std::boolalpha;
    std::cout << "Valid battery: " << valid_battery << '\n';
    std::cout << "Warning: " << warning << '\n';
}
