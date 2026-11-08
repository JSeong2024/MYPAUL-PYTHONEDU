#include <cmath>
#include <iostream>
#include <optional>

class TemperatureWindow {
public:
    [[nodiscard]] static std::optional<TemperatureWindow>
    create(double low, double high) noexcept {
        if (!std::isfinite(low) || !std::isfinite(high) || low > high) {
            return std::nullopt;
        }
        return TemperatureWindow{low, high};
    }

    [[nodiscard]] bool contains(double temperature) const noexcept {
        return std::isfinite(temperature) &&
               low_ <= temperature && temperature <= high_;
    }

private:
    TemperatureWindow(double low, double high) noexcept
        : low_{low}, high_{high} {}

    double low_{};
    double high_{};
};

int main() {
    const auto window = TemperatureWindow::create(18.0, 26.0);
    const auto invalid = TemperatureWindow::create(30.0, 10.0);
    std::cout << std::boolalpha;
    std::cout << "23 C allowed: " << (window && window->contains(23.0)) << '\n';
    std::cout << "Invalid range rejected: " << !invalid << '\n';
}
