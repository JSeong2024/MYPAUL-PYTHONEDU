#include <iostream>

class Alarm {
public:
    virtual ~Alarm() = default;
    [[nodiscard]] virtual bool triggered(int reading) const noexcept = 0;
};

class HighAlarm final : public Alarm {
public:
    [[nodiscard]] bool triggered(int reading) const noexcept override {
        return reading >= 80;
    }
};

int main() {
    const HighAlarm alarm;
    std::cout << std::boolalpha << "79: " << alarm.triggered(79)
              << ", 80: " << alarm.triggered(80) << '\n';
}
