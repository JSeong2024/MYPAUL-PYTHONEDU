#include <algorithm>
#include <print>

class Motor {
public:
    void set_speed(int rpm) noexcept { speed_ = std::clamp(rpm, 0, 3000); }
    [[nodiscard]] int speed() const noexcept { return speed_; }

private:
    int speed_{};
};

class Robot {
public:
    void drive(int rpm) noexcept { motor_.set_speed(rpm); }
    [[nodiscard]] int speed() const noexcept { return motor_.speed(); }

private:
    Motor motor_;
};

int main() {
    Robot robot;
    robot.drive(3500);
    std::println("RPM: {}", robot.speed());
    robot.drive(-100);
    std::println("After invalid input: {} RPM", robot.speed());
}
