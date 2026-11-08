#include <iostream>
#include <memory>
#include <vector>

class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};
class FixedSensor final : public Sensor {
public:
    explicit FixedSensor(int value) : value_{value} {}
    [[nodiscard]] int read() const noexcept override { return value_; }
private:
    int value_{};
};
[[nodiscard]] int count_high(const std::vector<std::unique_ptr<Sensor>>& sensors,
                             int threshold) {
    int count{};
    for (const auto& sensor : sensors) {
        if (sensor && sensor->read() >= threshold) ++count;
    }
    return count;
}
int main() {
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<FixedSensor>(75));
    sensors.push_back(std::make_unique<FixedSensor>(82));
    sensors.push_back(std::make_unique<FixedSensor>(90));
    std::cout << "High: " << count_high(sensors, 80) << '\n';
}
