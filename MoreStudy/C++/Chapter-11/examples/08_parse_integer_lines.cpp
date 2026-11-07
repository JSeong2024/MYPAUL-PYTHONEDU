#include <charconv>
#include <fstream>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] bool parse_int(std::string_view text, int& value) {
    if (text.empty()) return false;
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    return error == std::errc{} && end == text.data() + text.size();
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: parse_integer_lines <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    int value{};
    std::size_t line_number{};
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!parse_int(line, value)) {
            std::println(stderr, "Invalid integer at line {}", line_number);
            return 1;
        }
        std::println("Value: {}", value);
    }
    if (input.bad()) return 1;
}
