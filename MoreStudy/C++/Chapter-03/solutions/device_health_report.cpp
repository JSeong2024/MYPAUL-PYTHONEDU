#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    int battery_percent{};
    double temperature_c{};
    int raw_flags{};

    std::cout << "Battery (0-100): " << std::flush;
    if (!(std::cin >> battery_percent) ||
        battery_percent < 0 || battery_percent > 100) {
        std::cerr << "Error: battery must be 0-100.\n";
        return 1;
    }
    std::cout << "Temperature (-40 to 125 C): " << std::flush;
    if (!(std::cin >> temperature_c) ||
        !(temperature_c >= -40.0 && temperature_c <= 125.0)) {
        std::cerr << "Error: temperature must be -40 to 125.\n";
        return 1;
    }
    std::cout << "Flags (0-7): " << std::flush;
    if (!(std::cin >> raw_flags) || raw_flags < 0 || raw_flags > 7) {
        std::cerr << "Error: flags must be 0-7.\n";
        return 1;
    }

    const auto flags{static_cast<std::uint32_t>(raw_flags)};
    const bool power{(flags & power_on) != 0U};
    const bool sensor{(flags & sensor_ready) != 0U};
    const bool has_fault{(flags & fault) != 0U};

    std::cout << "\n--- Device Health ---\n";
    std::cout << "Battery: " << battery_percent << "%\n";
    std::cout << "Temperature: " << temperature_c << " C\n";
    std::cout << "Power: " << (power ? "ON" : "OFF") << '\n';
    std::cout << "Sensor: " << (sensor ? "READY" : "NOT READY") << '\n';
    std::cout << "Fault: " << (has_fault ? "YES" : "NO") << '\n';

    if (has_fault) {
        std::cout << "Status: FAULT\n";
    } else if (!power) {
        std::cout << "Status: POWER OFF\n";
    } else if (!sensor) {
        std::cout << "Status: SENSOR NOT READY\n";
    } else if (temperature_c >= 75.0) {
        std::cout << "Status: OVERHEAT\n";
    } else if (battery_percent <= 20) {
        std::cout << "Status: LOW BATTERY\n";
    } else {
        std::cout << "Status: READY\n";
    }
}
