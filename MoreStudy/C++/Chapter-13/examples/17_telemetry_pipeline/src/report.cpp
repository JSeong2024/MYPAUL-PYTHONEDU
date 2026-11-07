#include "telemetry/report.hpp"
#include <print>

namespace telemetry {
void report(std::string_view label, const Summary& summary) {
    std::println("{}: count={}, min={:.1f}, max={:.1f}, avg={:.1f}",
                 label, summary.count, summary.minimum, summary.maximum, summary.average);
}
} // namespace telemetry
