#include <print>
#include <string_view>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual std::string_view type() const noexcept = 0;
};

class DebugSensor final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "DebugSensor";
    }
    [[nodiscard]] int error_count() const noexcept { return 2; }
};

class SimpleSensor final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "SimpleSensor";
    }
};

void report(const Device& device) {
    if (const auto* debug = dynamic_cast<const DebugSensor*>(&device)) {
        std::println("{} errors: {}", device.type(), debug->error_count());
    } else {
        std::println("{} has no debug details", device.type());
    }
}

int main() {
    const DebugSensor debug;
    const SimpleSensor simple;
    report(debug);
    report(simple);
}
