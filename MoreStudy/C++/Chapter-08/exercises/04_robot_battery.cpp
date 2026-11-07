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
        // TODO: 1~1000m만 허용, 5m 이동마다 배터리 1% 소모(올림)
        // 배터리가 부족하면 이동하지 않고 잔량을 유지
        (void)distance_m;
        return false;
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
