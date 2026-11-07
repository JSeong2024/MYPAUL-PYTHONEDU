#include <cmath>
#include <optional>
#include <print>
#include <vector>

class SensorLog {
public:
    [[nodiscard]] bool add(double value) {
        if (!std::isfinite(value)) {
            return false;
        }
        samples_.push_back(value);
        return true;
    }

    [[nodiscard]] std::optional<double> average() const noexcept {
        if (samples_.empty()) {
            return std::nullopt;
        }
        double total{};
        for (const double value : samples_) {
            total += value;
        }
        return total / static_cast<double>(samples_.size());
    }

private:
    std::vector<double> samples_;
};

class Monitor {
public:
    [[nodiscard]] bool record(double value) { return log_.add(value); }
    [[nodiscard]] std::optional<double> average() const noexcept { return log_.average(); }

private:
    SensorLog log_;
};

int main() {
    Monitor monitor;
    const bool first = monitor.record(20.0);
    const bool second = monitor.record(24.0);
    if (!first || !second) {
        std::println("Invalid sample");
        return 1;
    }
    if (const auto avg = monitor.average()) {
        std::println("Average: {:.1f} C", *avg);
    }
}
