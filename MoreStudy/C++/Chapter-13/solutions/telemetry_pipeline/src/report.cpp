#include "telemetry/report.hpp"
#include <iomanip>
#include <iostream>

namespace telemetry {
void report(std::string_view label, const Summary& summary) {
    std::cout << label << ": count=" << summary.count
              << ", min=" << std::fixed << std::setprecision(1) << summary.minimum
              << ", max=" << summary.maximum << ", avg=" << summary.average << '\n';
}
}
