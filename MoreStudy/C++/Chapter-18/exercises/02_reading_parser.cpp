#include <optional>
#include <string>
#include <string_view>
struct Reading { std::string device; int value; };
// TODO: require READ <device> <integer>, device [A-Za-z0-9_-]{1,16}, value 0..1000.
// Reject extra tokens, trailing whitespace, and partially parsed numbers.
[[nodiscard]] std::optional<Reading> parse_reading(std::string_view text) {
    (void)text;
    return std::nullopt;
}
#ifndef CH18_LIBRARY_ONLY
#include <iostream>
int main() {
    auto result = parse_reading("READ motor-1 42");
    if (result) std::cout << result->device << ": " << result->value << '\n';
}
#endif
