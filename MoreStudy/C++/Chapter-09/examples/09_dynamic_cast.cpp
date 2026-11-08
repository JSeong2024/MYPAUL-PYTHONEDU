#include <iostream>

class Device {
public:
    virtual ~Device() = default;
};
class Camera final : public Device {
public:
    [[nodiscard]] int frames_per_second() const noexcept { return 60; }
};
class Motor final : public Device {};

void inspect(const Device& device) {
    const auto* camera = dynamic_cast<const Camera*>(&device);
    if (camera == nullptr) {
        std::cout << "Not a camera\n";
        return;
    }
    std::cout << "Camera FPS: " << camera->frames_per_second() << '\n';
}
int main() {
    const Camera camera;
    const Motor motor;
    inspect(camera);
    inspect(motor);
}
