#include <iostream>
#include <string_view>
[[nodiscard]] constexpr std::string_view build_mode() {
#ifdef NDEBUG
    return "Release-like";
#else
    return "Debug-like";
#endif
}
int main() {
    std::cout << "Mode: " << build_mode() << '\n';
}
