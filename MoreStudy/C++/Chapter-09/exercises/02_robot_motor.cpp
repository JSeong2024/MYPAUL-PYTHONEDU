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
        // TODO: 0~3000 범위일 때만 speed_를 변경하고 true를 반환하세요.
        (void)rpm;
        return false;
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
