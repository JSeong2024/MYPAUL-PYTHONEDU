#include <iostream>

enum class DeviceMode { off = 0, standby = 1, active = 2 };

int main() {
    int selected{};
    std::cout << "Mode (0-2): " << std::flush;
    if (!(std::cin >> selected) || selected < 0 || selected > 2) {
        std::cerr << "Error: mode must be 0-2.\n";
        return 1;
    }
    const DeviceMode mode{static_cast<DeviceMode>(selected)};
    switch (mode) {
        case DeviceMode::off:
            std::cout << "OFF\n";
            break;
        case DeviceMode::standby:
            std::cout << "STANDBY\n";
            break;
        case DeviceMode::active:
            std::cout << "ACTIVE\n";
            break;
    }
}
