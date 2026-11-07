#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Device {
    std::string_view id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    for (const auto& item : devices)
        std::println("{}: {}", item.id, item.priority);
}
