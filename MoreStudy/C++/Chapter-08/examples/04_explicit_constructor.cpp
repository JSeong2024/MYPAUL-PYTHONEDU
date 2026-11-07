#include <cstdint>
#include <print>

class DeviceId {
public:
    explicit DeviceId(std::uint32_t value) noexcept : value_{value} {}
    [[nodiscard]] std::uint32_t value() const noexcept { return value_; }

private:
    std::uint32_t value_{};
};

void print_device(DeviceId id) {
    std::println("Device ID: {}", id.value());
}

int main() {
    const DeviceId id{1'024};
    print_device(id);
    // print_device(1024); // explicit 생성자이므로 암묵적 변환 불가
}
