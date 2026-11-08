#include <iostream>

class Battery {
public:
    explicit Battery(int charge) noexcept
        : percent_{charge >= 0 && charge <= 100 ? charge : 0} {}

    [[nodiscard]] bool consume(int amount) noexcept {
        // TODO: 범위 검증 후 배터리를 소모하고, 부족하면 기존 값을 유지하세요.
        (void)amount;
        return false;
    }

    [[nodiscard]] int percent() const noexcept { return percent_; }

private:
    int percent_{};
};

class Robot {
public:
    explicit Robot(int charge) noexcept : battery_{charge} {}

    [[nodiscard]] bool move(int meters) noexcept {
        // TODO: 1~1000m만 허용하고, 5m당 배터리 1%를 올림 계산하세요.
        (void)meters;
        return false;
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
