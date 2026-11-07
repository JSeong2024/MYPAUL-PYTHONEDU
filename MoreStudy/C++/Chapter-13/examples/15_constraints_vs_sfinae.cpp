#include <concepts>
#include <print>
#include <type_traits>

// 구형 코드에서 흔히 보이는 형태
template <typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
[[nodiscard]] bool old_even(T value) { return value % 2 == 0; }

// 새 API에서 읽기 쉬운 제약 조건
template <typename T>
    requires std::integral<T>
[[nodiscard]] bool new_even(T value) { return value % 2 == 0; }

int main() {
    std::println("Old: {}, New: {}", old_even(6), new_even(7));
}
