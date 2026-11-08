#include "monitor.hpp"

namespace monitor {
std::string_view TemperatureSensor::kind() const noexcept { return "TEMP"; }
int TemperatureSensor::reading() const noexcept { return value_; }
bool TemperatureSensor::alert() const noexcept { return value_ >= 80; }
std::string_view DistanceSensor::kind() const noexcept { return "DIST"; }
int DistanceSensor::reading() const noexcept { return value_; }
bool DistanceSensor::alert() const noexcept { return value_ <= 30; }
Report evaluate(const std::vector<std::unique_ptr<Sensor>>& sensors) {
    Report report{};
    for (const auto& sensor : sensors) {
        if (!sensor) continue;
        ++report.total;
        if (sensor->alert()) ++report.alerts;
    }
    return report;
}
} // namespace monitor
