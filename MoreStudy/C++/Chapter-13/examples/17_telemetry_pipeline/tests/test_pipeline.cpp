#include "telemetry/pipeline.hpp"
#include <array>
#include <stdexcept>
#include <cmath>
#include <limits>
#include <vector>

struct Temperature {
    double measured;
    bool good;
    [[nodiscard]] double value() const noexcept { return measured; }
    [[nodiscard]] bool valid() const noexcept { return good; }
};
struct Pressure {
    float measured;
    [[nodiscard]] float value() const noexcept { return measured; }
    [[nodiscard]] bool valid() const noexcept { return true; }
};

static_assert(telemetry::ReadingLike<Temperature>);
static_assert(telemetry::ReadingLike<Pressure>);
static_assert(!telemetry::ReadingLike<int>);

void expect(bool condition, const char* description) {
    if (!condition) throw std::runtime_error(description);
}

int main() {
    const std::array batch{
        Temperature{28.0, true}, Temperature{999.0, false},
        Temperature{34.0, true}, Temperature{32.0, true}
    };
    const auto summary = telemetry::summarize(batch);
    expect(summary.has_value(), "test assertion failed");
    expect(summary->count == 3, "test assertion failed");
    expect(summary->minimum == 28.0, "test assertion failed");
    expect(summary->maximum == 34.0, "test assertion failed");
    expect(std::abs(summary->average - 94.0 / 3.0) < 1e-12, "test assertion failed");

    const std::vector<Temperature> empty;
    expect(!telemetry::summarize(empty).has_value(), "test assertion failed");
    const std::array all_invalid{Temperature{9.0, false}};
    expect(!telemetry::summarize(all_invalid).has_value(), "test assertion failed");
    const std::array nan_batch{
        Temperature{std::numeric_limits<double>::quiet_NaN(), true},
        Temperature{5.0, true}
    };
    const auto finite = telemetry::summarize(nan_batch);
    expect(finite && finite->count == 1 && finite->minimum == 5.0, "test assertion failed");
    const std::array pressures{Pressure{100.0f}, Pressure{102.0f}};
    const auto pressure = telemetry::summarize(pressures);
    expect(pressure && pressure->average == 101.0, "test assertion failed");
}
