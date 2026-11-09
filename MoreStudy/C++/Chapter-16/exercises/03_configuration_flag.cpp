#include <iostream>
#include <string_view>

[[nodiscard]] constexpr std::string_view feature_label() {
    // TODO: CH16_DIAGNOSTICS 매크로가 정의되면 "diagnostics-on", 아니면 "diagnostics-off".
    return "";
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << feature_label() << '\n'; }
#endif
