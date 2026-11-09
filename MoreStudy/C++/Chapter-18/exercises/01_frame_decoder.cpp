#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
// TODO: decode 4-byte big-endian length; reject incomplete/extra bytes and payloads over 4096.
[[nodiscard]] std::optional<std::string> decode(std::string_view packet) {
    (void)packet;
    return std::nullopt;
}
#ifndef CH18_LIBRARY_ONLY
#include <iostream>
int main() {
    std::string p{"\0\0\0\4PING",8};
    std::cout << decode(p).value_or("invalid") << '\n';
}
#endif
