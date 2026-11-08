#include <cmath>
#include <iostream>
#include <type_traits>

template <typename T>
[[nodiscard]] T clean_reading(T value) {
    if constexpr (std::is_floating_point_v<T>) {
        return std::isfinite(value) ? value : T{};
    } else {
        return value;
    }
}

int main() {
    std::cout << "Integer: " << clean_reading(12) << '\n';
    std::cout << "Invalid double: " << clean_reading(std::nan("")) << '\n';
}
