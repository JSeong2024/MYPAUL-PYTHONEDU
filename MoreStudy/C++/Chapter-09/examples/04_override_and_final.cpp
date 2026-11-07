#include <print>
#include <string_view>

class Alarm {
public:
    virtual ~Alarm() = default;
    [[nodiscard]] virtual std::string_view message() const = 0;
};

class TemperatureAlarm final : public Alarm {
public:
    [[nodiscard]] std::string_view message() const override {
        return "Temperature limit exceeded";
    }
};

int main() {
    const TemperatureAlarm alarm;
    const Alarm& base = alarm;
    std::println("{}", base.message());
}
