#include <iostream>
#include <stdexcept>
#include <string>

[[nodiscard]] std::string versioned_name(const std::string& name, int major) {
    if (name.empty() || major <= 0) throw std::invalid_argument("invalid name or version");
    return name + "-v" + std::to_string(major);
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << versioned_name("motor", 2) << '\n'; }
#endif
