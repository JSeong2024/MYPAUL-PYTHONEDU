#include <iostream>
#include <string_view>

[[nodiscard]] constexpr std::string_view feature_label() {
#ifdef CH16_DIAGNOSTICS
    return "diagnostics-on";
#else
    return "diagnostics-off";
#endif
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << feature_label() << '\n'; }
#endif
