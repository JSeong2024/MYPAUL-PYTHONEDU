#include <iomanip>
#include <iostream>
#include <string>

int main() {
    std::string device_name;
    double temperature_c{};
    double offset_c{};
    int samples{};

    std::cout << "Device: ";
    std::getline(std::cin, device_name);
    std::cout << "Temperature (C): ";
    std::cin >> temperature_c;
    std::cout << "Offset (C): ";
    std::cin >> offset_c;
    std::cout << "Samples: ";
    std::cin >> samples;

    const double adjusted_c{temperature_c + offset_c};
    const int whole_degrees{static_cast<int>(temperature_c)};

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "\n--- Measurement Card ---\n";
    std::cout << "Device: " << device_name << '\n';
    std::cout << "Temperature: " << temperature_c << " C\n";
    std::cout << "Offset: " << offset_c << " C\n";
    std::cout << "Adjusted: " << adjusted_c << " C\n";
    std::cout << "Samples: " << samples << '\n';
    std::cout << "Whole degrees: " << whole_degrees << '\n';
}
