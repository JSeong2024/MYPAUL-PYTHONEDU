#include <iostream>
#include <string_view>

[[nodiscard]] bool valid_package_name(std::string_view name) {
    if (name.empty()) return false;
    for (unsigned char ch : name) {
        const bool letter = (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z');
        const bool digit = ch >= '0' && ch <= '9';
        if (!letter && !digit && ch != '-') return false;
    }
    return true;
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << std::boolalpha << valid_package_name("sensor-core") << '\n'; }
#endif
