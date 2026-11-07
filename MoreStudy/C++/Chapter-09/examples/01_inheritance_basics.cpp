#include <print>
#include <string>
#include <string_view>
#include <utility>

class Device {
public:
    explicit Device(std::string id) : id_(std::move(id)) {}
    [[nodiscard]] std::string_view id() const noexcept { return id_; }

private:
    std::string id_;
};

class TemperatureSensor : public Device {
public:
    TemperatureSensor(std::string id, double celsius)
        : Device(std::move(id)), celsius_(celsius) {}

    [[nodiscard]] double read_celsius() const noexcept { return celsius_; }

private:
    double celsius_{};
};

int main() {
    const TemperatureSensor sensor{"TEMP-01", 24.5};
    std::println("{}: {:.1f} C", sensor.id(), sensor.read_celsius());
}
