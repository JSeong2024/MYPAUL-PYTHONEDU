#include <charconv>
#include <iostream>
#include <optional>
#include <string_view>
#include <system_error>

[[nodiscard]] std::optional<int> parse_port(std::string_view text) {
    if (text.empty()) return std::nullopt;
    int value{};
    const auto [end, error] = std::from_chars(text.data(), text.data()+text.size(), value);
    if (error != std::errc{} || end != text.data()+text.size() ||
        value < 1 || value > 65535) return std::nullopt;
    return value;
}
#ifndef CH13_LIBRARY_ONLY
int main() {
    std::cout << parse_port("8080").value_or(-1) << '\n';
}
#endif
