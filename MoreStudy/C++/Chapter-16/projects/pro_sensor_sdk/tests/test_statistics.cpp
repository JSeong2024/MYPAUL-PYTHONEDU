#include "sensor_sdk/statistics.hpp"
#include <array>
#include <stdexcept>
int main() {
    const std::array readings{10, 20, 30};
    const auto report = sensor_sdk::analyze(readings);
    if (report.count != 3 || report.minimum != 10 || report.maximum != 30 || report.average != 20.0) return 1;
    bool thrown = false;
    try { (void)sensor_sdk::analyze(std::array<int,0>{}); }
    catch (const std::invalid_argument&) { thrown = true; }
    if (!thrown) return 2;
    thrown = false;
    try { (void)sensor_sdk::analyze(std::array{1,1001}); }
    catch (const std::invalid_argument&) { thrown = true; }
    return thrown ? 0 : 3;
}
