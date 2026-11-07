#include <cmath>
#include <expected>
#include <print>
#include <string>

class TemperatureWindow {
public:
    [[nodiscard]] static std::expected<TemperatureWindow, std::string>
    create(double low, double high);

    [[nodiscard]] bool contains(double value) const noexcept {
        return std::isfinite(value) && low_ <= value && value <= high_;
    }

private:
    TemperatureWindow(double low, double high) noexcept : low_{low}, high_{high} {}
    double low_{};
    double high_{};
};

std::expected<TemperatureWindow, std::string>
TemperatureWindow::create(double low, double high) {
    if (!std::isfinite(low) || !std::isfinite(high) || low > high) {
        return std::unexpected("Invalid temperature range");
    }
    return TemperatureWindow{low, high};
}

int main() {
    const auto window = TemperatureWindow::create(18.0, 28.0);
    if (!window) {
        std::println("Error: {}", window.error());
        return 1;
    }
    std::println("23 C accepted: {}", window->contains(23.0));
    std::println("31 C accepted: {}", window->contains(31.0));
}
