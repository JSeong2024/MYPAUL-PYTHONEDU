#include <print>
#include <string_view>

class IAlarmChannel {
public:
    virtual ~IAlarmChannel() = default;
    virtual void notify(std::string_view message) const = 0;
};

class ConsoleAlarm final : public IAlarmChannel {
public:
    void notify(std::string_view message) const override {
        std::println("ALARM: {}", message);
    }
};

class SilentAlarm final : public IAlarmChannel {
public:
    void notify(std::string_view) const override {}
};

int main() {
    const ConsoleAlarm console;
    const SilentAlarm silent;
    const IAlarmChannel& first = console;
    const IAlarmChannel& second = silent;
    first.notify("High temperature");
    second.notify("High temperature");
}
