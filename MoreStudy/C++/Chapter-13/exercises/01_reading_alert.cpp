#include <cmath>
#include <concepts>
#include <iostream>

template <std::floating_point T>
[[nodiscard]] bool reading_alert(T value, T limit) {
    // TODO: 두 값이 모두 유한할 때만 value >= limit 판단
    (void)value;
    (void)limit;
    return false;
}

#ifndef CH13_LIBRARY_ONLY
int main() {
    std::cout << std::boolalpha << reading_alert(85.0, 80.0) << '\n';
}
#endif
