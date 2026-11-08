#include <iostream>

class Battery {
public:
    explicit Battery(int charge) noexcept
        : percent_{charge >= 0 && charge <= 100 ? charge : 0} {}

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
        if (meters < 1 || meters > 1'000) {
            return false;
        }
        const int cost{(meters + 4) / 5};
        return battery_.consume(cost);
    }

    [[nodiscard]] int battery_percent() const noexcept {
        return battery_.percent();
    }

private:
    Battery battery_;
};

int main() {
    Robot robot{100};
    const bool short_move{robot.move(25)};
    const bool long_move{robot.move(1'000)};
    std::cout << std::boolalpha << "Short: " << short_move
              << ", long: " << long_move
              << ", battery: " << robot.battery_percent() << "%\n";
}
