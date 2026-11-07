#include <charconv>
#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

template <std::integral T>
[[nodiscard]] std::expected<T, std::errc> parse(std::string_view text) {
    T value{};
    const auto [ptr, ec] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (ec != std::errc{}) return std::unexpected(ec);
    if (ptr != text.data() + text.size()) return std::unexpected(std::errc::invalid_argument);
    return value;
}

int main() {
    for (const std::string_view text : {"120", "-7", "12ms", "99999999999999999999999"}) {
        const auto result = parse<int>(text);
        if (result) std::println("{} -> {}", text, *result);
        else std::println("{} -> error", text);
    }
}
