#include <cmath>
#include <expected>
#include <print>
#include <string>

class TemperatureWindow {
public:
    [[nodiscard]] static std::expected<TemperatureWindow, std::string>
    create(double lower, double upper);

    [[nodiscard]] bool contains(double value) const noexcept {
        return std::isfinite(value) && lower_ <= value && value <= upper_;
    }

private:
    TemperatureWindow(double lower, double upper) noexcept
        : lower_{lower}, upper_{upper} {}

    double lower_{};
    double upper_{};
};

std::expected<TemperatureWindow, std::string>
TemperatureWindow::create(double lower, double upper) {
    if (!std::isfinite(lower) || !std::isfinite(upper) || lower > upper) {
        return std::unexpected("Invalid temperature range");
    }
    return TemperatureWindow{lower, upper};
}

int main() {
    const auto window = TemperatureWindow::create(18.0, 28.0);
    if (!window) {
        std::println("Error: {}", window.error());
        return 1;
    }
    std::println("23 C allowed: {}", window->contains(23.0));
}
