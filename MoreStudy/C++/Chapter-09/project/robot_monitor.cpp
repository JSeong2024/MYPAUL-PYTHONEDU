#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual bool alert() const noexcept = 0;
    [[nodiscard]] virtual const char* kind() const noexcept = 0;
    [[nodiscard]] virtual int value() const noexcept = 0;
};
class TemperatureSensor final : public Sensor {
public:
    explicit TemperatureSensor(int value) : value_{value} {}
    [[nodiscard]] bool alert() const noexcept override {
        // TODO: 온도가 80 이상이면 경고
        return false;
    }
    [[nodiscard]] const char* kind() const noexcept override { return "TEMP"; }
    [[nodiscard]] int value() const noexcept override { return value_; }
private:
    int value_{};
};
class DistanceSensor final : public Sensor {
public:
    explicit DistanceSensor(int value) : value_{value} {}
    [[nodiscard]] bool alert() const noexcept override {
        // TODO: 거리가 30 이하이면 경고
        return false;
    }
    [[nodiscard]] const char* kind() const noexcept override { return "DIST"; }
    [[nodiscard]] int value() const noexcept override { return value_; }
private:
    int value_{};
};
[[nodiscard]] int count_alerts(const std::vector<std::unique_ptr<Sensor>>& sensors) {
    // TODO: 다형성 호출을 이용하여 경고 센서 개수를 구하세요.
    (void)sensors;
    return 0;
}
int main() {
    int count{};
    std::cout << "Sensors (1-5): " << std::flush;
    if (!(std::cin >> count) || count < 1 || count > 5) {
        std::cerr << "Error: invalid count\n";
        return 1;
    }
    std::vector<std::unique_ptr<Sensor>> sensors;
    for (int i = 1; i <= count; ++i) {
        std::string type;
        int value{};
        std::cout << "Sensor " << i << " (TEMP/DIST value): " << std::flush;
        if (!(std::cin >> type >> value)) {
            std::cerr << "Error: invalid reading\n";
            return 1;
        }
        if (type == "TEMP" && value >= -40 && value <= 125) {
            sensors.push_back(std::make_unique<TemperatureSensor>(value));
        } else if (type == "DIST" && value >= 0 && value <= 400) {
            sensors.push_back(std::make_unique<DistanceSensor>(value));
        } else {
            std::cerr << "Error: invalid sensor\n";
            return 1;
        }
    }
    std::cout << "--- Robot Sensor Monitor ---\n";
    for (const auto& sensor : sensors) {
        std::cout << sensor->kind() << ' ' << sensor->value() << ": "
                  << (sensor->alert() ? "ALERT" : "CLEAR") << '\n';
    }
    std::cout << "Total: " << sensors.size() << '\n';
    std::cout << "Alerts: " << count_alerts(sensors) << '\n';
}
