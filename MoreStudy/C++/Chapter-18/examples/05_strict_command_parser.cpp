#include <charconv>
#include <iostream>
#include <string_view>
#include <system_error>
[[nodiscard]] bool parse_port(std::string_view text, int& port) {
    if (text.empty()) return false;
    const char* first = text.data();
    const char* last = first + text.size();
    const auto [end, error] = std::from_chars(first, last, port);
    return error == std::errc{} && end == last && port >= 1 && port <= 65535;
}
int main() {
    int port = 0;
    std::cout << std::boolalpha
              << "valid: " << parse_port("8080", port) << " / " << port << '\n'
              << "invalid: " << parse_port("8080x", port) << '\n';
}
