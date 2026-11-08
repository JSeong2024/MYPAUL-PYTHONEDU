#include <iostream>
#include <memory>
#include <string>
#include <utility>

struct Device {
    std::string name;
    explicit Device(std::string value) : name(std::move(value)) {}
};

void inspect(const Device& device) {
    std::cout << "Device: " << device.name << '\n';
}

int main() {
    auto owner = std::make_unique<Device>("Motor-A");
    inspect(*owner);
    auto next_owner = std::move(owner);
    std::cout << std::boolalpha << "Old owner empty: " << (owner == nullptr) << '\n';
    inspect(*next_owner);
}
