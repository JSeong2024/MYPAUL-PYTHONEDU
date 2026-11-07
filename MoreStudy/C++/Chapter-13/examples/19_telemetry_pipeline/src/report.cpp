#include "telemetry/pipeline.hpp"
#include <print>

namespace telemetry {

void print_report(const std::vector<Reading>& readings) {
    const auto result = summarize(readings);
    if (!result) {
        std::println("No valid readings");
        return;
    }
    std::println("Valid: {}", result->count);
    std::println("Min: {:.1f}, max: {:.1f}, avg: {:.1f}",
                 result->minimum, result->maximum, result->average);
}

} // namespace telemetry
