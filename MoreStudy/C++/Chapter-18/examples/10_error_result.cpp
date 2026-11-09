#include <iostream>
#include <optional>
#include <string_view>
[[nodiscard]] std::optional<int> parse_status(std::string_view text) {
    if (text == "OK") return 200;
    if (text == "BAD_REQUEST") return 400;
    return std::nullopt;
}
int main() {
    std::cout << "Known: " << parse_status("OK").value() << '\n';
    std::cout << "Unknown: " << std::boolalpha << !parse_status("?" ) << '\n';
}
