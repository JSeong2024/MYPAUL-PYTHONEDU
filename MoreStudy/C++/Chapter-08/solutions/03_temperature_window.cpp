#include <cmath>
#include <iostream>
#include <optional>

class TemperatureWindow {
public:
    [[nodiscard]] static std::optional<TemperatureWindow>
    create(double lower, double upper) noexcept {
        if (!std::isfinite(lower) || !std::isfinite(upper) || lower > upper) {
            return std::nullopt;
        }
        return TemperatureWindow{lower, upper};
    }

    [[nodiscard]] bool contains(double value) const noexcept {
        return std::isfinite(value) && lower_ <= value && value <= upper_;
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
