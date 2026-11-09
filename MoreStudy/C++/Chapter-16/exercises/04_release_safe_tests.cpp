#include <iostream>
#include <string_view>

[[nodiscard]] bool valid_package_name(std::string_view name) {
    // TODO: 비어 있지 않으며, 문자[A-Z, a-z, 0-9, -]로만 이루어져야 함.
    (void)name;
    return false;
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << std::boolalpha << valid_package_name("sensor-core") << '\n'; }
#endif
