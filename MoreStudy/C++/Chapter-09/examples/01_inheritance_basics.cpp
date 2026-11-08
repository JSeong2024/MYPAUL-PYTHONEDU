#include <iostream>
#include <string>
#include <utility>

class Device {
public:
    explicit Device(std::string id) : id_{std::move(id)} {}
    [[nodiscard]] const std::string& id() const noexcept { return id_; }
private:
    std::string id_;
};

class TemperatureSensor : public Device {
public:
    TemperatureSensor(std::string id, double celsius)
        : Device{std::move(id)}, celsius_{celsius} {}
    [[nodiscard]] double celsius() const noexcept { return celsius_; }
private:
    double celsius_{};
};

int main() {
    const TemperatureSensor sensor{"TEMP-01", 24.5};
    std::cout << sensor.id() << ": " << sensor.celsius() << " C\n";
}
