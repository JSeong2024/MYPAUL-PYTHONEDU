#include <charconv>
#include <expected>
#include <print>
#include <string_view>

[[nodiscard]] std::expected<int, std::string_view>
parse_percentage(std::string_view input) {
    int value{};
    const auto [end, error] = std::from_chars(
        input.data(), input.data() + input.size(), value);

    if (error != std::errc{} || end != input.data() + input.size()) {
        return std::unexpected("not an integer");
    }
    if (value < 0 || value > 100) {
        return std::unexpected("out of range (0..100)");
    }
    return value;
}

int main() {
    for (const std::string_view input : {"85", "85%", "120"}) {
        const auto result = parse_percentage(input);
        if (result) {
            std::println("{} -> {}", input, *result);
        } else {
            std::println("{} -> error: {}", input, result.error());
        }
    }
}
