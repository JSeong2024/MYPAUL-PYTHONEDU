#include <charconv>
#include <iostream>
#include <string>
#include <system_error>
int main() {
    const std::string text{"42"};
    int value{};
    const auto result = std::from_chars(text.data(),text.data()+text.size(),value);
    if (result.ec != std::errc{} || result.ptr != text.data()+text.size()) { return 1; }
    std::cout << "Reading: " << value << '\n';
}
