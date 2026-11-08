#include <iostream>

class Battery {
public:
    explicit Battery(int percent) noexcept : percent_{percent} {}

    [[nodiscard]] bool consume(int amount) noexcept {
        if (amount < 0 || amount > percent_) {
            return false;
        }
        percent_ -= amount;
        return true;
    }

    [[nodiscard]] int percent() const noexcept { return percent_; }

private:
    int percent_{};
};

class Robot {
public:
    explicit Robot(int charge) noexcept : battery_{charge} {}

    [[nodiscard]] bool move(int meters) noexcept {
        if (meters <= 0 || meters > 100) {
            return false;
        }
        return battery_.consume((meters + 4) / 5);
    }

    [[nodiscard]] int battery_percent() const noexcept {
        return battery_.percent();
    }

private:
    Battery battery_;
};

int main() {
    Robot robot{30};
    const bool moved{robot.move(25)};
    std::cout << std::boolalpha << "Moved: " << moved
              << ", battery: " << robot.battery_percent() << "%\n";
}
