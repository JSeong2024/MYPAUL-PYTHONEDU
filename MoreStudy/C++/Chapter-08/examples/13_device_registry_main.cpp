#include "13_device_registry.hpp"

#include <print>

int main() {
    DeviceRegistry registry;
    const bool first = registry.add("CAM-01");
    const bool duplicate = registry.add("CAM-01");
    const bool second = registry.add("LIDAR-02");
    std::println("First: {}, duplicate: {}, second: {}", first, duplicate, second);
    std::println("Registered: {}", registry.size());
}
