#include <iostream>

class Battery {
public:
    explicit Battery(int percent) : percent_{percent} {}
    [[nodiscard]] bool consume(int amount) noexcept {
        if (amount < 0 || amount > percent_) return false;
        percent_ -= amount;
        return true;
    }
    [[nodiscard]] int percent() const noexcept { return percent_; }
private:
    int percent_{};
};
class Robot {
public:
    explicit Robot(int battery_percent) : battery_{battery_percent} {}
    [[nodiscard]] bool move() noexcept { return battery_.consume(10); }
    [[nodiscard]] int battery() const noexcept { return battery_.percent(); }
private:
    Battery battery_;
};
int main() {
    Robot robot{35};
    const bool moved = robot.move();
    std::cout << std::boolalpha << "Moved: " << moved << ", battery: "
              << robot.battery() << "%\n";
}
