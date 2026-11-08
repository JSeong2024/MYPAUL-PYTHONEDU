#include <iostream>

class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual const char* kind() const noexcept { return "generic"; }
};

class DistanceSensor final : public Sensor {
public:
    [[nodiscard]] const char* kind() const noexcept override { return "distance"; }
};

void print_kind(const Sensor& sensor) {
    std::cout << "Sensor: " << sensor.kind() << '\n';
}

int main() {
    const Sensor basic;
    const DistanceSensor distance;
    print_kind(basic);
    print_kind(distance);
}
