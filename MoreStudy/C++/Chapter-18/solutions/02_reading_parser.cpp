#include <charconv>
#include <optional>
#include <string>
#include <string_view>
#include <system_error>
struct Reading { std::string device; int value; };
[[nodiscard]] std::optional<Reading> parse_reading(std::string_view text) {
    // Strictly: READ <device> <integer> (no extra whitespace / tokens).
    if (!text.starts_with("READ ")) return std::nullopt;
    text.remove_prefix(5);
    const auto separator = text.find(' ');
    if (separator == std::string_view::npos || separator < 1 || separator > 16)
        return std::nullopt;
    const auto device = text.substr(0, separator);
    for (unsigned char c : device) {
        if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
              (c >= '0' && c <= '9') || c == '_' || c == '-')) return std::nullopt;
    }
    text.remove_prefix(separator + 1);
    int value = 0;
    if (text.empty()) return std::nullopt;
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{} || end != text.data() + text.size() || value < 0 || value > 1000)
        return std::nullopt;
    return Reading{std::string(device), value};
}
#ifndef CH18_LIBRARY_ONLY
#include <iostream>
int main() {
    auto result = parse_reading("READ motor-1 42");
    if (result) std::cout << result->device << ": " << result->value << '\n';
}
#endif
