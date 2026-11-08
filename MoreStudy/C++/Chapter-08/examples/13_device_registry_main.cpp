#include "13_device_registry.hpp"

#include <iostream>

int main() {
    DeviceRegistry registry;
    const bool first{registry.add("CAM-01")};
    const bool duplicate{registry.add("CAM-01")};
    const bool second{registry.add("LIDAR-02")};
    std::cout << std::boolalpha
              << "First: " << first << ", duplicate: " << duplicate
              << ", second: " << second << '\n';
    std::cout << "Registered: " << registry.size() << '\n';
}
