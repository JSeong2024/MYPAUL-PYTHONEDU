#include "telemetry.hpp"
#include <stdexcept>
#include <string>
#include <vector>
void check(bool b) { if (!b) throw std::runtime_error("telemetry check failed"); }
int main() {
    std::string device; int value = 0;
    check(telemetry::parse("READ sensor-1 0", device, value));
    check(device == "sensor-1" && value == 0);
    check(!telemetry::parse("READ sensor-1 1001", device, value));
    check(!telemetry::parse("READ bad! 3", device, value));
    check(!telemetry::parse("READ A 2 ", device, value));
    check(!telemetry::parse("READ A 2x", device, value));
    check(!telemetry::parse("READ A -1", device, value));
    const auto result = telemetry::collect({"READ A 20", "READ B 30", "READ A 5", "READ BAD x"});
    check(result.accepted == 3 && result.rejected == 1);
    check(result.devices.at("A").count == 2 && result.devices.at("A").sum == 25);
    check(result.devices.at("B").sum == 30);
    check(telemetry::collect({}).accepted == 0);
    try { (void)telemetry::collect(std::vector<std::string>(33, "READ A 1")); }
    catch (const std::invalid_argument&) { return 0; }
    return 1;
}
