#include <print>

class Motor {
public:
    void set_speed(int rpm) noexcept {
        // TODO: rpm을 0~3000으로 제한하고 speed_에 저장합니다.
        (void)rpm;
    }
    [[nodiscard]] int speed() const noexcept { return speed_; }

private:
    int speed_{};
};

class Robot {
public:
    void drive(int rpm) noexcept {
        // TODO: motor_의 메서드를 호출합니다.
        (void)rpm;
    }
    [[nodiscard]] int speed() const noexcept { return motor_.speed(); }

private:
    Motor motor_;
};

int main() {
    Robot robot;
    robot.drive(3500);
    std::println("RPM: {}", robot.speed());
}
