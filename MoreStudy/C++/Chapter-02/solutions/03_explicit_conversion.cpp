#include <iostream>

int main() {
    double reading{};
    std::cout << "Reading: ";
    std::cin >> reading;

    const int whole_part{static_cast<int>(reading)};
    std::cout << "Original: " << reading << '\n';
    std::cout << "Whole part: " << whole_part << '\n';
}
