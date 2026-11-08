#include <iostream>

class Controller {
public:
    [[nodiscard]] int speed() const noexcept { return speed_; }
protected:
    void set_speed_unchecked(int speed) noexcept { speed_ = speed; }
private:
    int speed_{};
};

class FanController final : public Controller {
public:
    [[nodiscard]] bool request_speed(int rpm) noexcept {
        if (rpm < 0 || rpm > 3000) return false;
        set_speed_unchecked(rpm);
        return true;
    }
};

int main() {
    FanController fan;
    const bool accepted = fan.request_speed(1200);
    const bool rejected = fan.request_speed(-1);
    std::cout << std::boolalpha << "Accepted: " << accepted
              << ", rejected: " << rejected << ", speed: " << fan.speed() << '\n';
}
