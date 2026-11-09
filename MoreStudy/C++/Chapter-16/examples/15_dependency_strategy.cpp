#include <charconv>
#include <iostream>
#include <string_view>
[[nodiscard]] bool read_number(std::string_view input, int& output) {
    const char* first = input.data();
    const char* last = first + input.size();
    const auto [ptr, ec] = std::from_chars(first, last, output);
    return ec == std::errc{} && ptr == last;
}
int main() {
    int value{};
    std::cout << "Parsed: " << std::boolalpha << read_number("120", value)
              << ", value=" << value << '\n';
}
