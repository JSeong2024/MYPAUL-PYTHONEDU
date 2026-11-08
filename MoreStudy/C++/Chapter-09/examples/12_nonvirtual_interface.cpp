#include <iostream>

class AlarmRule {
public:
    virtual ~AlarmRule() = default;
    [[nodiscard]] bool check(int reading) const noexcept {
        if (reading < 0 || reading > 100) return false;
        return check_valid(reading);
    }
private:
    [[nodiscard]] virtual bool check_valid(int reading) const noexcept = 0;
};
class HighAlarm final : public AlarmRule {
private:
    [[nodiscard]] bool check_valid(int reading) const noexcept override {
        return reading >= 80;
    }
};
int main() {
    const HighAlarm alarm;
    std::cout << std::boolalpha << "Invalid: " << alarm.check(110)
              << ", high: " << alarm.check(90) << '\n';
}
