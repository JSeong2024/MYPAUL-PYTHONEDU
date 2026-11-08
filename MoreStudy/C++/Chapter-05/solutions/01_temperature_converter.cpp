#include <iomanip>
#include <iostream>

double to_fahrenheit(double celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    double celsius{};
    if (!(std::cin >> celsius)) {
        std::cerr << "Error: invalid temperature.\n";
        return 1;
    }
    std::cout << std::fixed << std::setprecision(1)
              << "Fahrenheit: " << to_fahrenheit(celsius) << '\n';
}
