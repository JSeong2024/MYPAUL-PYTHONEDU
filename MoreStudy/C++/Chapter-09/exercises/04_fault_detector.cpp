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
    // TODO: 측정값이 없거나 유한하지 않으면 false
    // TODO: 유효한 측정값이 threshold보다 크면 true
    (void)source;
    (void)threshold;
    return false;
}

int main() {
    const FakeReading sensor{85.0};
    std::println("Overheated: {}", is_overheated(sensor, 80.0));
}
