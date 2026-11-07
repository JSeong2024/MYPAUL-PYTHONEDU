#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <print>

int main() {
    constexpr std::array<std::int64_t, 4> packets{
        1'000'000, 2'000'000, 3'000'000, 4'000'000
    };
    std::int64_t total{};

    for (const std::int64_t packet_count : packets) {
        if (packet_count < 0 ||
            total > std::numeric_limits<std::int64_t>::max() - packet_count) {
            std::cerr << "Error: invalid packet count or overflow.\n";
            return 1;
        }
        total += packet_count;
    }

    std::println("Packets: {}", total);
}
