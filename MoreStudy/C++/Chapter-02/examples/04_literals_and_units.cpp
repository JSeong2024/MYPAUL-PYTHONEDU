#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t serial_baud{115'200};
    constexpr int retry_limit{3};
    constexpr double max_distance_m{2.5};
    constexpr std::uint8_t status_mask{0b0000'0101};

    std::println("Serial baud: {}", serial_baud);
    std::println("Retries: {}", retry_limit);
    std::println("Maximum distance: {:.1f} m", max_distance_m);
    std::println("Status mask: {}", static_cast<unsigned int>(status_mask));
}
