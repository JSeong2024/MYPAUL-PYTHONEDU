#pragma once
#include "telemetry/pipeline.hpp"
#include <string_view>

namespace telemetry {
void report(std::string_view label, const Summary& summary);
}
