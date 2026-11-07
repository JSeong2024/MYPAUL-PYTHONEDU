#include <charconv>
#include <cstdint>
#include <expected>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::expected<std::uint16_t, std::string>
parse_port(std::string_view text) {
    unsigned int value{};
    const auto [ptr, ec] = std::from_chars(text.data(),
                                            text.data() + text.size(), value);

    if (ec != std::errc{} || ptr != text.data() + text.size() ||
        value == 0 || value > 65'535) {
        return std::unexpected("Port must be an integer from 1 to 65535");
    }
    return static_cast<std::uint16_t>(value);
}

int main() {
    for (const std::string_view input : {"8080", "70000"}) {
        const auto result = parse_port(input);
        if (result) {
            std::println("Port: {}", *result);
        } else {
            std::println("Error: {}", result.error());
        }
    }
}
