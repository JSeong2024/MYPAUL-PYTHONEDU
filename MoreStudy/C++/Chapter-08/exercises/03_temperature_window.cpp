#include <cmath>
#include <iostream>
#include <optional>

class TemperatureWindow {
public:
    [[nodiscard]] static std::optional<TemperatureWindow>
    create(double lower, double upper) noexcept {
        // TODO: 유한한 범위이며 lower <= upper일 때만 객체를 반환하세요.
        (void)lower;
        (void)upper;
        return std::nullopt;
    }

    [[nodiscard]] bool contains(double value) const noexcept {
        // TODO: 유한한 값이 [lower_, upper_]에 속하는지 확인하세요.
        (void)value;
        (void)lower_;
        (void)upper_;
        return false;
    }

private:
    TemperatureWindow(double lower, double upper) noexcept
        : lower_{lower}, upper_{upper} {}

    double lower_{};
    double upper_{};
};

int main() {
    const auto window = TemperatureWindow::create(15.0, 25.0);
    std::cout << std::boolalpha << "23 C allowed: "
              << (window && window->contains(23.0)) << '\n';
}
