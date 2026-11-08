#include <cstdint>
#include <iostream>

class DeviceId {
public:
    explicit DeviceId(std::uint32_t value) noexcept : value_{value} {}

    [[nodiscard]] std::uint32_t value() const noexcept { return value_; }

private:
    std::uint32_t value_{};
};

void print_device(DeviceId id) {
    std::cout << "Device ID: " << id.value() << '\n';
}

int main() {
    const DeviceId id{1'024};
    print_device(id);
    // print_device(1024); // explicit이므로 암묵적 변환은 허용되지 않음.
}
