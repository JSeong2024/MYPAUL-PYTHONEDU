#include <charconv>
#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

template <std::integral T>
    requires (!std::same_as<T, bool>)
[[nodiscard]] std::expected<T, std::errc> parse_number(std::string_view text) {
    T result{};
    const auto [end, ec] = std::from_chars(text.data(), text.data() + text.size(), result);
    if (ec != std::errc{}) return std::unexpected(ec);
    if (end != text.data() + text.size())
        return std::unexpected(std::errc::invalid_argument);
    return result;
}

int main() {
    const auto ok = parse_number<int>("2048");
    const auto bad = parse_number<int>("10ms");
    std::println("Parsed: {}", ok.value());
    std::println("Rejected suffix: {}", !bad);
}
