#include <algorithm>
#include <iterator>
#include <print>
#include <ranges>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}, {"lidar", 4}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    auto filtered = devices | std::views::filter([](const Device& item) {
        return item.priority >= 3;
    });
#ifdef __cpp_lib_ranges_to_container
    const auto selected = filtered | std::ranges::to<std::vector<Device>>();
#else
    std::vector<Device> selected;
    std::ranges::copy(filtered, std::back_inserter(selected));
#endif
    std::println("Selected: {}", selected.size());
    for (const auto& item : selected) std::println("{}: {}", item.id, item.priority);
}
