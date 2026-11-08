#include <concepts>
#include <iostream>
#include <type_traits>

template <typename T>
std::enable_if_t<std::is_integral_v<T>, bool> legacy_even(T value) {
    return value % 2 == 0;
}

template <std::integral T>
[[nodiscard]] bool modern_even(T value) { return value % 2 == 0; }

int main() {
    std::cout << std::boolalpha << "Legacy: " << legacy_even(6) << '\n';
    std::cout << "Concept: " << modern_even(6) << '\n';
}
