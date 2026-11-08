#include <algorithm>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int reading;
    bool active;
};

[[nodiscard]] std::vector<Device> selected_devices(const std::vector<Device>& source,
                                                    int threshold) {
    std::vector<Device> output;
    for (const auto& device : source) {
        if (device.active && device.reading >= threshold) output.push_back(device);
    }
    std::ranges::sort(output, {}, &Device::id);
    return output;
}
#ifndef CH13_LIBRARY_ONLY
int main() {
    const std::vector<Device> data{{"B", 80, true}, {"A", 90, true}, {"C", 99, false}};
    for (const auto& d : selected_devices(data, 80)) std::cout << d.id << '\n';
}
#endif
