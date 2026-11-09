#include "device/report.hpp"
#include <array>
#include <stdexcept>

int main() {
    const std::array readings{device::Record{"A", 20}, device::Record{"B", 95}};
    const auto summary = device::summarize(readings, 90);
    if (summary.count != 2 || summary.alerts != 1 || summary.total != 115) return 1;
    const std::array<device::Record, 0> empty{};
    if (device::summarize(empty, 80).count != 0) return 2;
    bool rejected = false;
    try { (void)device::summarize(readings, 101); }
    catch (const std::invalid_argument&) { rejected = true; }
    if (!rejected) return 3;
    rejected = false;
    try { (void)device::summarize(std::array{device::Record{"A", -1}}, 80); }
    catch (const std::invalid_argument&) { rejected = true; }
    return rejected ? 0 : 4;
}
