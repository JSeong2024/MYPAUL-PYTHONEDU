#include <iomanip>
#include <iostream>

int main() {
    double raw_c{};
    double offset_c{};

    std::cout << "Temperature (C): ";
    std::cin >> raw_c;
    std::cout << "Offset (C): ";
    std::cin >> offset_c;

    const double adjusted_c{raw_c + offset_c};
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Original: " << raw_c << " C\n";
    std::cout << "Adjusted: " << adjusted_c << " C\n";
}
