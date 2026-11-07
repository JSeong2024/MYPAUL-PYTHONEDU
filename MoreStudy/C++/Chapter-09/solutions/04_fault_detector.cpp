#include <cmath>
#include <limits>
#include <optional>
#include <print>

struct IReadingSource {
    virtual ~IReadingSource() = default;
    [[nodiscard]] virtual std::optional<double> read() const = 0;
};

class FakeReading final : public IReadingSource {
public:
    explicit FakeReading(std::optional<double> value) : value_(value) {}
    [[nodiscard]] std::optional<double> read() const override { return value_; }

private:
    std::optional<double> value_;
};

[[nodiscard]] bool is_overheated(const IReadingSource& source,
                                 double threshold) {
    if (!std::isfinite(threshold)) return false;
    const auto value = source.read();
    return value && std::isfinite(*value) && *value > threshold;
}

int main() {
    const FakeReading hot{85.0};
    const FakeReading normal{70.0};
    const FakeReading missing{std::nullopt};
    const FakeReading invalid{std::numeric_limits<double>::quiet_NaN()};

    std::println("Hot: {}", is_overheated(hot, 80.0));
    std::println("Normal: {}", is_overheated(normal, 80.0));
    std::println("Missing: {}", is_overheated(missing, 80.0));
    std::println("Invalid: {}", is_overheated(invalid, 80.0));
}
