#include <iostream>

class Motor {
public:
    virtual ~Motor() = default;
    [[nodiscard]] virtual bool set_speed(int rpm) noexcept = 0;
    [[nodiscard]] virtual int speed() const noexcept = 0;
};
class ElectricMotor final : public Motor {
public:
    [[nodiscard]] bool set_speed(int rpm) noexcept override {
        if (rpm < 0 || rpm > 3000) return false;
        speed_ = rpm;
        return true;
    }
    [[nodiscard]] int speed() const noexcept override { return speed_; }
private:
    int speed_{};
};
int main() {
    ElectricMotor motor;
    Motor& control = motor;
    const bool first = control.set_speed(2000);
    const bool second = control.set_speed(3500);
    std::cout << std::boolalpha << "First: " << first << ", second: "
              << second << ", RPM: " << control.speed() << '\n';
}
