#include <iostream>

enum class DeviceMode { off, standby, active };

int main() {
    constexpr DeviceMode mode{DeviceMode::standby};

    switch (mode) {
        case DeviceMode::off:
            std::cout << "Power off\n";
            break;
        case DeviceMode::standby:
            std::cout << "Waiting for input\n";
            break;
        case DeviceMode::active:
            std::cout << "Device active\n";
            break;
    }
}
