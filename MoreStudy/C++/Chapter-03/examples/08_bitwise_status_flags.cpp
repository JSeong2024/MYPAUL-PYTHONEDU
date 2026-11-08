#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    std::uint32_t flags{power_on};
    flags |= sensor_ready;
    const bool ready{(flags & (power_on | sensor_ready)) ==
                     (power_on | sensor_ready)};
    flags |= fault;
    flags &= ~fault;

    std::cout << std::boolalpha;
    std::cout << "Ready: " << ready << '\n';
    std::cout << "Flags: " << flags << '\n';
    std::cout << "Fault set: " << ((flags & fault) != 0U) << '\n';
}
