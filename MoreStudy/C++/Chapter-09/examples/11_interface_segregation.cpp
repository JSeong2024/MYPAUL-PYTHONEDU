#include <print>

struct IReadable {
    virtual ~IReadable() = default;
    [[nodiscard]] virtual double read() const = 0;
};

struct ICalibratable {
    virtual ~ICalibratable() = default;
    virtual void calibrate(double offset) = 0;
};

class AdjustableSensor final : public IReadable, public ICalibratable {
public:
    explicit AdjustableSensor(double raw) : raw_(raw) {}
    [[nodiscard]] double read() const override { return raw_ + offset_; }
    void calibrate(double offset) override { offset_ = offset; }

private:
    double raw_{};
    double offset_{};
};

class FixedSensor final : public IReadable {
public:
    [[nodiscard]] double read() const override { return 20.0; }
};

void display(const IReadable& sensor) {
    std::println("Reading: {:.1f}", sensor.read());
}

int main() {
    AdjustableSensor adjustable{21.0};
    adjustable.calibrate(1.5);
    const FixedSensor fixed;
    display(adjustable);
    display(fixed);
}
