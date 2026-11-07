#include <charconv>
#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

template <std::integral T>
[[nodiscard]] std::expected<T, std::errc> parse_integer(std::string_view text) {
    T value{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{}) return std::unexpected(error);
    if (end != text.data() + text.size()) return std::unexpected(std::errc::invalid_argument);
    return value;
}

int main() {
    const auto good = parse_integer<int>("2048");
    const auto bad = parse_integer<int>("10ms");
    if (good) std::println("Value: {}", *good);
    std::println("Invalid input: {}", !bad);
}
