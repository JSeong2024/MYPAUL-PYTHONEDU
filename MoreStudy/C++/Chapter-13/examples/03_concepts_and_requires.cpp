#include <concepts>
#include <iostream>

template <std::integral T>
[[nodiscard]] bool is_even(T value) { return value % 2 == 0; }

template <std::floating_point T>
[[nodiscard]] T midpoint(T left, T right) {
    return left + (right - left) / T{2};
}

int main() {
    std::cout << std::boolalpha << "Even: " << is_even(12) << '\n';
    std::cout << "Midpoint: " << midpoint(1.0, 3.0) << '\n';
    // is_even(2.5); // std::integral 제약을 만족하지 않아 컴파일되지 않음
}
