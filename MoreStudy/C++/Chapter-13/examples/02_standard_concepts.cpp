#include <concepts>
#include <print>

template <std::integral T>
[[nodiscard]] constexpr bool is_even(T value) noexcept {
    return value % 2 == 0;
}

template <std::floating_point T>
[[nodiscard]] constexpr T average(T left, T right) noexcept {
    return left / T{2} + right / T{2};
}

static_assert(is_even(42));
static_assert(average(2.0, 4.0) == 3.0);

int main() {
    std::println("Even: {}", is_even(42));
    std::println("Average: {}", average(2.0, 4.0));
}
