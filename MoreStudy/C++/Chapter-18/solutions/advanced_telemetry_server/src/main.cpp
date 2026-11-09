#include "telemetry.hpp"
#include <iostream>
int main() {
    auto result = telemetry::collect({"READ A 20", "READ B 30", "READ A 5", "READ BAD x"});
    std::cout << "Accepted: " << result.accepted << ", Rejected: " << result.rejected << '\n';
    for (const auto& [device, data] : result.devices)
        std::cout << device << ": " << data.count << " / " << data.sum << '\n';
}
