#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int reading;
};

int main() {
    std::vector<Device> devices{{"B", 4}, {"A", 8}, {"C", 2}};
    std::ranges::sort(devices, {}, &Device::id);
    for (const auto& device : devices) {
        std::cout << device.id << ':' << device.reading << ' ';
    }
    std::cout << '\n';
}
