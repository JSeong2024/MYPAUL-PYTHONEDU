#include <print>
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
    const std::vector<std::string> devices{"lidar", "camera", "imu"};
    if (const auto* result = find_device(devices, "camera")) {
        std::println("Found: {}", *result);
    }
    std::println("Missing: {}", find_device(devices, "gps") == nullptr);
}
