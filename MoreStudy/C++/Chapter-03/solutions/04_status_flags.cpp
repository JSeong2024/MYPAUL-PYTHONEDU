#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};
    int raw_flags{};

    std::cout << "Flags (0-7): " << std::flush;
    if (!(std::cin >> raw_flags) || raw_flags < 0 || raw_flags > 7) {
        std::cerr << "Error: flags must be 0-7.\n";
        return 1;
    }
    const auto flags{static_cast<std::uint32_t>(raw_flags)};
    if ((flags & fault) != 0U) {
        std::cout << "FAULT\n";
    } else if ((flags & (power_on | sensor_ready)) ==
               (power_on | sensor_ready)) {
        std::cout << "READY\n";
    } else {
        std::cout << "NOT READY\n";
    }
}
