#include <charconv>
#include <iostream>
#include <optional>
#include <string_view>
#include <system_error>

[[nodiscard]] std::optional<int> parse_port(std::string_view text) {
    if (text.empty()) return std::nullopt;
    int port{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), port);
    if (error != std::errc{} || end != text.data() + text.size() ||
        port < 1 || port > 65535) return std::nullopt;
    return port;
}

int main() {
    std::cout << "Port: " << parse_port("8080").value_or(-1) << '\n';
    std::cout << "Invalid: " << parse_port("80x").has_value() << '\n';
}
