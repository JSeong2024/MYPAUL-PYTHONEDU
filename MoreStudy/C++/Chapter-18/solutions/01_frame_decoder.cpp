#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
[[nodiscard]] std::optional<std::string> decode(std::string_view packet) {
    if (packet.size() < 4) return std::nullopt;
    std::uint32_t n = 0;
    for (std::size_t i = 0; i < 4; ++i)
        n = (n << 8) | static_cast<unsigned char>(packet[i]);
    if (n > 4096 || packet.size() - 4 != n) return std::nullopt;
    return std::string{packet.substr(4)};
}
#ifndef CH18_LIBRARY_ONLY
#include <iostream>
int main() {
    std::string p{"\0\0\0\4PING",8};
    std::cout << decode(p).value_or("invalid") << '\n';
}
#endif
