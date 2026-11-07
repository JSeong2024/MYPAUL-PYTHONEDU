#include <print>
#include <string>
#include <utility>

class Battery {
public:
    [[nodiscard]] bool consume(int percentage) noexcept {
        if (percentage <= 0 || percentage > remaining_) {
            return false;
        }
        remaining_ -= percentage;
        return true;
    }

    [[nodiscard]] int remaining() const noexcept { return remaining_; }

private:
    int remaining_{100};
};

class Robot {
public:
    explicit Robot(std::string id) : id_{std::move(id)} {}

    [[nodiscard]] bool travel(int distance_m) noexcept {
        if (distance_m < 1 || distance_m > 1'000) {
            return false;
        }
        const int cost = (distance_m + 4) / 5;
        return battery_.consume(cost);
    }

    [[nodiscard]] int battery_percent() const noexcept {
        return battery_.remaining();
    }

private:
    std::string id_;
    Battery battery_;
};

int main() {
    Robot robot{"ROBOT-A"};
    const bool short_trip = robot.travel(25);
    const bool long_trip = robot.travel(1'000);
    std::println("Short: {}, long: {}, battery: {}%",
                 short_trip, long_trip, robot.battery_percent());
}
