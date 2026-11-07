#include <concepts>
#include <print>
#include <type_traits>

// 함수 인수의 참조/const를 제거한 타입을 기준으로 검사
template <typename T>
constexpr bool is_numeric_v =
    std::integral<std::remove_cvref_t<T>> ||
    std::floating_point<std::remove_cvref_t<T>>;

int main() {
    const int value{7};
    static_assert(is_numeric_v<decltype((value))>);
    static_assert(!is_numeric_v<const char*>);
    std::println("Value: {}, numeric: {}", value, is_numeric_v<decltype((value))>);
}
