#include <cstdio>
#include "event_summary.hpp"
#include <print>
#include <vector>

int main() {
    const std::vector<Event> events{
        {"LIDAR", 48}, {"CAMERA", 87}, {"LIDAR", 110},
        {"CAMERA", 35}, {"IMU", 12}
    };
    const auto result = summarize_events(events, 80);
    if (!result) {
        std::println(stderr, "Error: {}", result.error());
        return 1;
    }
    for (const auto& summary : *result) {
        std::println("{}: count={}, slow={}, mean={:.1f} ms",
                     summary.device, summary.count, summary.slow_count,
                     summary.mean_ms());
    }
}
