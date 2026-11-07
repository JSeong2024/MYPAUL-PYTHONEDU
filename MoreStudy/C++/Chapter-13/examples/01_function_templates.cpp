#include <concepts>
#include <print>

template <typename T>
[[nodiscard]] constexpr T max_value(const T& left, const T& right) {
    return left < right ? right : left;
}

int main() {
    std::println("Maximum int: {}", max_value(12, 19));
    std::println("Maximum double: {}", max_value(1.5, 2.75));
    // max_value(1, 2.0); // T를 하나로 추론할 수 없음
    std::println("Explicit T: {}", max_value<double>(1, 2.5));
}
