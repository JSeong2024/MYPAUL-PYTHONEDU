#include <cstdint>
#include <limits>
#include <print>

int main() {
    const std::uint32_t device_id{1'024};
    const std::int64_t uptime_ms{86'400'000};

    std::println("Device ID: {}", device_id);
    std::println("Uptime: {} ms", uptime_ms);
    std::println("uint16_t maximum: {}",
                 std::numeric_limits<std::uint16_t>::max());
}
