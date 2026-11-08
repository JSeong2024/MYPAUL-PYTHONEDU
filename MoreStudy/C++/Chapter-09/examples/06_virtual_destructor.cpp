#include <iostream>
#include <memory>

class Device {
public:
    virtual ~Device() { std::cout << "Device closed\n"; }
};

class Camera final : public Device {
public:
    ~Camera() override { std::cout << "Camera closed\n"; }
};

int main() {
    std::unique_ptr<Device> device = std::make_unique<Camera>();
    std::cout << "Using camera\n";
}
