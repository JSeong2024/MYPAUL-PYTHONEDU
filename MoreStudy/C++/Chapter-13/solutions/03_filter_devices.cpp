#include <algorithm>
#include <print>
#include <ranges>
#include <string>
#include <vector>

struct Device { std::string name; int priority; };

int main() {
    std::vector<Device> devices{{"camera", 3}, {"motor", 1}, {"lidar", 5}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    auto selected = devices | std::views::filter([](const Device& d) { return d.priority >= 3; })
                            | std::ranges::to<std::vector>();
    for (const auto& device : selected) {
        std::println("{}: {}", device.name, device.priority);
    }
}
