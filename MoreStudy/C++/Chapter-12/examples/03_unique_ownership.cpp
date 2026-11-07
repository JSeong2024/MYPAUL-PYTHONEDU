#include <memory>
#include <print>
#include <string>
#include <utility>

struct Device {
    std::string name;
    explicit Device(std::string value) : name(std::move(value)) {}
};

void inspect(const Device& device) {
    std::println("Device: {}", device.name);
}

int main() {
    auto owner = std::make_unique<Device>("Motor-A");
    inspect(*owner); // 대여: Ownership 이동 없음

    auto next_owner = std::move(owner);
    std::println("Old owner empty: {}", owner == nullptr);
    inspect(*next_owner);
}
