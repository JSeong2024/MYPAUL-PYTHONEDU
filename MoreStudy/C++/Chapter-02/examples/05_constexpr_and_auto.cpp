#include <cstdint>
#include <print>
#include <string>

int main() {
    constexpr int samples_per_second{50};
    constexpr int milliseconds_per_second{1'000};
    constexpr auto interval_ms = milliseconds_per_second / samples_per_second;

    const std::string sensor_name{"IMU-01"};
    auto sample_count = std::uint32_t{120};

    std::println("Sensor: {}", sensor_name);
    std::println("Interval: {} ms", interval_ms);
    std::println("Samples: {}", sample_count);
}
