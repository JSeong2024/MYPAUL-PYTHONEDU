#include "telemetry/pipeline.hpp"
#include "telemetry/report.hpp"
#include <array>
#include <vector>

struct TemperatureReading {
    double celsius;
    bool okay;
    [[nodiscard]] double value() const noexcept { return celsius; }
    [[nodiscard]] bool valid() const noexcept { return okay; }
};
struct PressureReading {
    float kilopascal;
    bool okay;
    [[nodiscard]] float value() const noexcept { return kilopascal; }
    [[nodiscard]] bool valid() const noexcept { return okay; }
};

int main() {
    const std::array temperatures{
        TemperatureReading{28.0, true}, TemperatureReading{32.0, false},
        TemperatureReading{34.0, true}, TemperatureReading{32.0, true}
    };
    const std::vector pressures{
        PressureReading{100.0f, true}, PressureReading{102.0f, true}
    };
    if (const auto summary = telemetry::summarize(temperatures))
        telemetry::report("Temperature", *summary);
    if (const auto summary = telemetry::summarize(pressures))
        telemetry::report("Pressure", *summary);
}
