#include <algorithm>
#include <print>

class AlarmConfig {
public:
    AlarmConfig& set_threshold(int value) noexcept {
        threshold_ = std::clamp(value, 0, 100);
        return *this;
    }

    AlarmConfig& enable(bool value) noexcept {
        enabled_ = value;
        return *this;
    }

    [[nodiscard]] bool triggered(int reading) const noexcept {
        return enabled_ && reading >= threshold_;
    }

private:
    int threshold_{80};
    bool enabled_{true};
};

int main() {
    AlarmConfig config;
    config.set_threshold(65).enable(true);
    std::println("Alarm at 70: {}", config.triggered(70));
}
