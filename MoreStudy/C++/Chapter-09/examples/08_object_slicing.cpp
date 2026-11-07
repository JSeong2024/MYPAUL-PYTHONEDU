#include <print>
#include <string_view>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual std::string_view type() const noexcept {
        return "Device";
    }
};

class Camera final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "Camera";
    }
};

void by_value(Device device) {
    std::println("By value: {}", device.type());
}

void by_reference(const Device& device) {
    std::println("By reference: {}", device.type());
}

int main() {
    const Camera camera;
    by_value(camera);      // 파생 클래스 부분이 복사되지 않음
    by_reference(camera);  // 원본의 실제 타입 유지
}
