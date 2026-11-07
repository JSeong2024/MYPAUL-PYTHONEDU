#include "monitor.hpp"

#include <algorithm>
#include <cmath>
#include <ranges>
#include <utility>

TemperatureSensor::TemperatureSensor(std::string id, double celsius)
    : id_(std::move(id)), celsius_(celsius) {}

std::string_view TemperatureSensor::id() const noexcept { return id_; }
std::string_view TemperatureSensor::unit() const noexcept { return "C"; }
std::optional<double> TemperatureSensor::read() const noexcept {
    if (!std::isfinite(celsius_)) return std::nullopt;
    return celsius_;
}

BatterySensor::BatterySensor(std::string id, double percent)
    : id_(std::move(id)), percent_(percent) {}

std::string_view BatterySensor::id() const noexcept { return id_; }
std::string_view BatterySensor::unit() const noexcept { return "%"; }
std::optional<double> BatterySensor::read() const noexcept {
    if (!std::isfinite(percent_) || percent_ < 0.0 || percent_ > 100.0) {
        return std::nullopt;
    }
    return percent_;
}

bool Monitor::add(std::unique_ptr<ISensor> sensor) {
    if (!sensor || sensor->id().empty()) return false;
    const bool duplicate = std::ranges::any_of(sensors_, [&](const auto& stored) {
        return stored->id() == sensor->id();
    });
    if (duplicate) return false;

    sensors_.push_back(std::move(sensor));
    return true;
}

std::vector<Sample> Monitor::collect() const {
    std::vector<Sample> result;
    result.reserve(sensors_.size());
    for (const auto& sensor : sensors_) {
        result.push_back(Sample{
            std::string{sensor->id()}, sensor->read(), std::string{sensor->unit()}
        });
    }
    return result;
}
