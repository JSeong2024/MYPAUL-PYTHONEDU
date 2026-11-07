#include "telemetry/pipeline.hpp"
#include <array>
#include <limits>
#include <vector>

struct ExternalReading { const char* device; double value; bool valid; };
static_assert(telemetry::ReadingLike<ExternalReading>);
static_assert(!telemetry::ReadingLike<int>);

int main() {
    const std::array<ExternalReading, 4> readings{{
        {"A", 10.0, true},
        {"B", 20.0, true},
        {"C", 999.0, false},
        {"D", std::numeric_limits<double>::quiet_NaN(), true}
    }};
    const auto summary = telemetry::summarize(readings);
    if (!summary || summary->count != 2 || summary->minimum != 10.0 ||
        summary->maximum != 20.0 || summary->average != 15.0) return 1;
    const std::vector<telemetry::Reading> empty;
    if (telemetry::summarize(empty)) return 2;
}
