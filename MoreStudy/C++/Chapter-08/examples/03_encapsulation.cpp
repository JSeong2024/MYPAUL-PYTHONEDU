#include <iostream>

class Motor {
public:
    [[nodiscard]] bool set_rpm(int requested) noexcept {
        if (requested < 0 || requested > 3'000) {
            return false;
        }
        rpm_ = requested;
        return true;
    }

    [[nodiscard]] int rpm() const noexcept { return rpm_; }

private:
    int rpm_{};
};

int main() {
    Motor motor;
    const bool accepted{motor.set_rpm(1'500)};
    const bool rejected{motor.set_rpm(4'000)};
    std::cout << std::boolalpha << "Accepted: " << accepted
              << ", rejected: " << rejected
              << ", RPM: " << motor.rpm() << '\n';
}
