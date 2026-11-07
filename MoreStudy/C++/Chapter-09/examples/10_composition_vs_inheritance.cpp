#include <algorithm>
#include <print>
#include <string>
#include <string_view>
#include <utility>

class Motor {
public:
    void set_rpm(int requested) noexcept {
        rpm_ = std::clamp(requested, 0, 3'000);
    }
    [[nodiscard]] int rpm() const noexcept { return rpm_; }

private:
    int rpm_{};
};

class Robot {
public:
    explicit Robot(std::string name) : name_(std::move(name)) {}
    void move(int requested_rpm) noexcept { motor_.set_rpm(requested_rpm); }
    [[nodiscard]] std::string_view name() const noexcept { return name_; }
    [[nodiscard]] int motor_rpm() const noexcept { return motor_.rpm(); }

private:
    std::string name_;
    Motor motor_;  // Robot은 Motor를 소유함
};

int main() {
    Robot robot{"Cleaner-A"};
    robot.move(3'500);
    std::println("{} motor: {} RPM", robot.name(), robot.motor_rpm());
}
