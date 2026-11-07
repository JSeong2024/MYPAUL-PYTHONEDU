#include <functional>
#include <optional>
#include <print>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] std::optional<std::reference_wrapper<std::string>>
find_mutable(std::vector<std::string>& devices, std::string_view target) {
    for (auto& device : devices) {
        if (device == target) {
            return std::ref(device);
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<std::string> devices{"camera", "lidar"};
    if (auto found = find_mutable(devices, "lidar")) {
        found->get() = "lidar-front";
    }
    std::println("Renamed: {}", devices.at(1));
}
