#include <algorithm>
#include <print>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    for (const auto& device : devices) {
        std::println("{}: {}", device.id, device.priority);
    }
}
