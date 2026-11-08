#include <iostream>

int main() {
    constexpr int battery_percent{20};
    constexpr int warning_limit{20};

    std::cout << std::boolalpha;
    std::cout << "At warning limit: " << (battery_percent == warning_limit) << '\n';
    std::cout << "Low battery: " << (battery_percent <= warning_limit) << '\n';
    std::cout << "Above limit: " << (battery_percent > warning_limit) << '\n';
}
