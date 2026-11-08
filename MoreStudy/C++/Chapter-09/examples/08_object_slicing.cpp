#include <iostream>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual const char* kind() const noexcept { return "device"; }
};
class Camera final : public Device {
public:
    [[nodiscard]] const char* kind() const noexcept override { return "camera"; }
};

void by_value(Device copy) { std::cout << "By value: " << copy.kind() << '\n'; }
void by_reference(const Device& device) {
    std::cout << "By reference: " << device.kind() << '\n';
}
int main() {
    const Camera camera;
    by_value(camera);  // 파생 부분이 복사되지 않는 객체 슬라이싱
    by_reference(camera);
}
