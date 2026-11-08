#include <charconv>
#include <iostream>
#include <string_view>
#include <system_error>

[[nodiscard]] bool parse_int(std::string_view text, int& value) {
    const char* first = text.data();
    const char* last = first + text.size();
    const auto [next, error] = std::from_chars(first, last, value);
    return error == std::errc{} && next == last;
}

int main() {
    for (const std::string_view text : {"42", "42ms", "-7"}) {
        int result{};
        if (parse_int(text, result)) {
            std::cout << "Accepted: " << result << '\n';
        } else {
            std::cout << "Rejected: " << text << '\n';
        }
    }
}
