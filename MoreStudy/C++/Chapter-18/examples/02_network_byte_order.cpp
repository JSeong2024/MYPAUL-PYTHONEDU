#include <cstdint>
#include <iostream>
int main() {
    constexpr std::uint32_t size = 0x01020304;
    std::cout << std::hex << static_cast<unsigned>((size >> 24) & 0xff) << ' '
              << static_cast<unsigned>((size >> 16) & 0xff) << ' '
              << static_cast<unsigned>((size >> 8) & 0xff) << ' '
              << static_cast<unsigned>(size & 0xff) << '\n';
}
