#include <cmath>
#include <concepts>
#include <iostream>

template <std::floating_point T>
[[nodiscard]] bool reading_alert(T value, T limit) {
    return std::isfinite(value) && std::isfinite(limit) && value >= limit;
}
#ifndef CH13_LIBRARY_ONLY
int main() {
    std::cout << std::boolalpha << reading_alert(85.0, 80.0) << '\n';
}
#endif
