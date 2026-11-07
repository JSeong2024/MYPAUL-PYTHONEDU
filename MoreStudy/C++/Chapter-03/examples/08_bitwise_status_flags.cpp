#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    constexpr std::uint32_t status{power_on | sensor_ready};

    const bool ready = (status & (power_on | sensor_ready)) ==
                           (power_on | sensor_ready) &&
                       (status & fault) == 0U;

    std::println("Status flags: {}", status);
    std::println("Device ready: {}", ready);
}
