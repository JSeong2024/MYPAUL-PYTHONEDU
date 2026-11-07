#include "telemetry/pipeline.hpp"
#include <array>
#include <print>
#include <vector>

int main() {
    const std::array samples{
        telemetry::Reading{"motor", 32.0, true},
        telemetry::Reading{"camera", 28.0, true},
        telemetry::Reading{"lidar", 0.0, false},
        telemetry::Reading{"motor", 34.0, true}
    };
    const auto summary = telemetry::summarize(samples);
    if (!summary) return 1;
    std::println("Array average: {:.1f}", summary->average);
    telemetry::print_report(std::vector<telemetry::Reading>{samples.begin(), samples.end()});
}
