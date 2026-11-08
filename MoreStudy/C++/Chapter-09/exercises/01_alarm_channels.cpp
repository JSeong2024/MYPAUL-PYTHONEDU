#include <iostream>

class Alarm {
public:
    virtual ~Alarm() = default;
    [[nodiscard]] virtual bool triggered(int reading) const noexcept = 0;
};
class HighAlarm final : public Alarm {
public:
    explicit HighAlarm(int threshold) : threshold_{threshold} {}
    [[nodiscard]] bool triggered(int reading) const noexcept override {
        // TODO: reading이 threshold_ 이상일 때만 true를 반환하세요.
        (void)reading;
        return false;
    }
private:
    int threshold_{};
};
int main() {
    const HighAlarm alarm{80};
    const Alarm& rule = alarm;
    std::cout << std::boolalpha << "79: " << rule.triggered(79)
              << ", 80: " << rule.triggered(80) << '\n';
}
