#include <cmath>
#include <expected>
#include <print>
#include <string_view>

class Controller {
public:
    virtual ~Controller() = default;

    [[nodiscard]] std::expected<double, std::string_view>
    apply(double requested) const {
        if (!std::isfinite(requested) || requested < 0.0 || requested > 100.0) {
            return std::unexpected("Input must be from 0 to 100");
        }
        return transform(requested);
    }

private:
    [[nodiscard]] virtual double transform(double value) const = 0;
};

class ScaleController final : public Controller {
private:
    [[nodiscard]] double transform(double value) const override {
        return value * 0.8;
    }
};

int main() {
    const ScaleController controller;
    for (const double requested : {75.0, 150.0}) {
        if (const auto result = controller.apply(requested)) {
            std::println("Output: {:.1f}", *result);
        } else {
            std::println("Error: {}", result.error());
        }
    }
}
