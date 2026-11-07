#include <cstdint>
#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    std::cout << "Status flags (0-15): " << std::flush;
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::cerr << "Error: missing input.\n";
        return 1;
    }

    int raw_status{};
    const auto parsed = std::from_chars(
        line.data(), line.data() + line.size(), raw_status);
    if (parsed.ec != std::errc{} ||
        parsed.ptr != line.data() + line.size() ||
        raw_status < 0 || raw_status > 15) {
        std::cerr << "Error: invalid status flags.\n";
        return 1;
    }

    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};
    const auto status = static_cast<std::uint32_t>(raw_status);

    if ((status & fault) != 0U) {
        std::println("FAULT");
    } else if ((status & (power_on | sensor_ready)) ==
               (power_on | sensor_ready)) {
        std::println("READY");
    } else {
        std::println("NOT READY");
    }
}
