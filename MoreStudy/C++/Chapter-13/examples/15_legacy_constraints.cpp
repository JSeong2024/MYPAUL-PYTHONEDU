#include <concepts>
#include <print>
#include <type_traits>

// 레거시 API의 SFINAE 제약 (읽기 위한 예시)
template <typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
[[nodiscard]] constexpr bool old_is_even(T value) { return value % 2 == 0; }

// 신규 C++20+ API의 권장 표현
template <std::integral T>
[[nodiscard]] constexpr bool is_even(T value) { return value % 2 == 0; }

int main() {
    std::println("Legacy: {}", old_is_even(6));
    std::println("Modern: {}", is_even(7));
}
