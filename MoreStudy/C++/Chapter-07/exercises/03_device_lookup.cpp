#include <iostream>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices, std::string_view target) {
    // TODO: return a pointer to the first matching element, or nullptr.
    (void)devices;
    (void)target;
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
