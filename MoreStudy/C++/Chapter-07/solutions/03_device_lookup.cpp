#include <iostream>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices, std::string_view target) {
    for (const auto& device : devices) {
        if (device == target) {
            return &device;
        }
    }
    return nullptr;
}

int main() {
    const std::vector<std::string> devices{"camera", "imu", "lidar"};
    if (const auto* found = find_device(devices, "imu")) {
        std::cout << "Found: " << *found << '\n';
    }
    std::cout << std::boolalpha;
    std::cout << "Missing: " << (find_device(devices, "gps") == nullptr) << '\n';
}
