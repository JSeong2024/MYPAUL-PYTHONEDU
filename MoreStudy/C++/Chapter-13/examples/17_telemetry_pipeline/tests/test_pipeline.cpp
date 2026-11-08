#include "telemetry/pipeline.hpp"
#include <array>
#include <cmath>
#include <limits>
#include <stdexcept>
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

void expect(bool condition) {
    if (!condition) throw std::runtime_error("pipeline test failed");
}

int main() {
    const std::array batch{
        Temperature{28.0, true}, Temperature{999.0, false},
        Temperature{34.0, true}, Temperature{32.0, true}
    };
    const auto result = telemetry::summarize(batch);
    expect(result.has_value());
    expect(result->count == 3);
    expect(result->minimum == 28.0 && result->maximum == 34.0);
    expect(std::abs(result->average - 94.0/3.0) < 1e-12);

    const std::vector<Temperature> empty;
    expect(!telemetry::summarize(empty));
    const std::array invalid{Temperature{9.0, false}};
    expect(!telemetry::summarize(invalid));
    const std::array nan_values{
        Temperature{std::numeric_limits<double>::quiet_NaN(), true},
        Temperature{5.0, true}
    };
    auto finite = telemetry::summarize(nan_values);
    expect(finite && finite->count == 1 && finite->average == 5.0);
    const std::array pressures{Pressure{100.0f}, Pressure{102.0f}};
    auto pressure = telemetry::summarize(pressures);
    expect(pressure && pressure->average == 101.0);
}
