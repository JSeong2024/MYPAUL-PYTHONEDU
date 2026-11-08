#include <cstdint>
#include <iostream>
#include <vector>
int main() {
    const std::uint32_t value{0x12345678u};
    const std::vector<std::uint8_t> bytes{
        static_cast<std::uint8_t>((value >> 24) & 0xffu),
        static_cast<std::uint8_t>((value >> 16) & 0xffu),
        static_cast<std::uint8_t>((value >> 8) & 0xffu),
        static_cast<std::uint8_t>(value & 0xffu)};
    std::uint32_t restored{};
    for (const auto byte : bytes) { restored = (restored << 8) | byte; }
    std::cout << std::boolalpha << "Round trip: " << (value == restored) << '\n';
}
