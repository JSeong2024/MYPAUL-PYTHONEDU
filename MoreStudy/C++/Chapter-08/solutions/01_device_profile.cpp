#include <cmath>
#include <iostream>
#include <string>

struct DeviceProfile {
    std::string name;
    double power_w{};
    bool online{};

    [[nodiscard]] bool valid() const noexcept {
        return !name.empty() && std::isfinite(power_w) &&
               power_w >= 0.0 && power_w <= 2'000.0;
    }
};

int main() {
    const DeviceProfile first{"Vacuum-A", 850.0, true};
    const DeviceProfile second{"", 850.0, false};
    std::cout << std::boolalpha
              << "Valid: " << first.valid()
              << ", invalid: " << second.valid() << '\n';
}
