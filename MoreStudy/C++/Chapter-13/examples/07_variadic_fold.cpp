#include <concepts>
#include <print>

template <typename... T>
    requires (std::convertible_to<T, double> && ...)
[[nodiscard]] constexpr double sum_samples(T... values) {
    return (0.0 + ... + static_cast<double>(values));
}

int main() {
    std::println("Total: {}", sum_samples(3, 4.5, 2));
    std::println("Empty total: {}", sum_samples());
}
