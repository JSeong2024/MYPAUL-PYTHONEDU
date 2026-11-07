#include <array>
#include <bit>
#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t number{0x01020304};
    const std::array<std::uint8_t, 4> bytes{
        static_cast<std::uint8_t>(number >> 24),
        static_cast<std::uint8_t>(number >> 16),
        static_cast<std::uint8_t>(number >> 8),
        static_cast<std::uint8_t>(number)
    };
    std::println("Network bytes: {:02X} {:02X} {:02X} {:02X}",
                 bytes[0], bytes[1], bytes[2], bytes[3]);
    if constexpr (std::endian::native == std::endian::little) {
        std::println("Host: Little Endian");
    } else if constexpr (std::endian::native == std::endian::big) {
        std::println("Host: Big Endian");
    } else {
        std::println("Host: Mixed/Other Endian");
    }
}
