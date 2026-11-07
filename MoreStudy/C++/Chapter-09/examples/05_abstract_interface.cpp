#include <optional>
#include <print>

class IReadingSource {
public:
    virtual ~IReadingSource() = default;
    [[nodiscard]] virtual std::optional<double> read() const = 0;
};

class SimulatedTemperature final : public IReadingSource {
public:
    explicit SimulatedTemperature(double value) : value_(value) {}
    [[nodiscard]] std::optional<double> read() const override {
        return value_;
    }

private:
    double value_;
};

void display(const IReadingSource& source) {
    if (const auto result = source.read()) {
        std::println("Reading: {:.1f} C", *result);
    } else {
        std::println("Reading unavailable");
    }
}

int main() {
    const SimulatedTemperature sensor{22.5};
    display(sensor);
}
