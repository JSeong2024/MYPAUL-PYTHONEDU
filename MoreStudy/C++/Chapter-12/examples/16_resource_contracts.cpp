#include <iostream>
#include <memory>
#include <string>
#include <utility>

struct Device { std::string name; };

void inspect(const Device& value) { // 접근만 수행: 비소유
    std::cout << "Inspect: " << value.name << '\n';
}

void register_device(std::unique_ptr<Device> device) { // 소유권 인수
    inspect(*device);
    std::cout << "Registered\n";
}

int main() {
    auto device = std::make_unique<Device>(Device{"Pump-A"});
    inspect(*device);
    register_device(std::move(device));
    std::cout << std::boolalpha << "Owner empty: " << (device == nullptr) << '\n';
}
