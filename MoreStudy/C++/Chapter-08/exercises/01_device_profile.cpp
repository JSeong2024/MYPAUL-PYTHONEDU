#include <cmath>
#include <iostream>
#include <string>

struct DeviceProfile {
    std::string name;
    double power_w{};
    bool online{};

    [[nodiscard]] bool valid() const noexcept {
        // TODO: 이름이 비어 있지 않고, 전력이 유한한 0~2000 W인지 확인하세요.
        return false;
    }
};

int main() {
    const DeviceProfile first{"Vacuum-A", 850.0, true};
    const DeviceProfile second{"", 850.0, false};
    std::cout << std::boolalpha
              << "Valid: " << first.valid()
              << ", invalid: " << second.valid() << '\n';
}
