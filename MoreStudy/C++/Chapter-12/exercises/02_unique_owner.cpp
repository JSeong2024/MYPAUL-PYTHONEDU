#include <memory>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#ifndef CH12_LIBRARY_ONLY
#include <iostream>
#endif

struct Device { std::string name; };

class DeviceRegistry {
public:
    // 전달받은 unique_ptr의 독점 소유권을 Registry가 인수합니다.
    void install(std::unique_ptr<Device> device) {
        // TODO 1: nullptr 또는 빈 이름이면 std::invalid_argument를 발생시킵니다.
        // TODO 2: 유효한 device를 std::move로 device_에 보관합니다.
        (void)device;
    }
    [[nodiscard]] bool has_device() const noexcept { return static_cast<bool>(device_); }
    [[nodiscard]] std::string_view name() const noexcept {
        return device_ ? std::string_view{device_->name} : std::string_view{};
    }
private:
    std::unique_ptr<Device> device_;
};

#ifndef CH12_LIBRARY_ONLY
int main() {
    DeviceRegistry registry;
    auto device = std::make_unique<Device>(Device{"Motor-A"});
    registry.install(std::move(device));
    std::cout << "Device: " << registry.name() << '\n';
    std::cout << std::boolalpha << "Old owner empty: " << (device == nullptr) << '\n';
}
#endif
