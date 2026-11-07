#include "monitor.hpp"

#include <cstdio>
#include <memory>
#include <print>

int main() {
    Monitor monitor;
    if (!monitor.add(std::make_unique<TemperatureSensor>("TEMP-A", 23.5)) ||
        !monitor.add(std::make_unique<BatterySensor>("BAT-A", 87.0)) ||
        !monitor.add(std::make_unique<BatterySensor>("BAT-B", 150.0))) {
        std::println(stderr, "Failed to register a sensor");
        return 1;
    }

    for (const auto& sample : monitor.collect()) {
        if (sample.value) {
            std::println("{}: {:.1f} {}", sample.id, *sample.value, sample.unit);
        } else {
            std::println("{}: unavailable", sample.id);
        }
    }
}
