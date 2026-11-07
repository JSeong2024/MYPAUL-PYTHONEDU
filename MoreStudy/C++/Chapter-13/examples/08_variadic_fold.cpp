#include <concepts>
#include <print>

template <typename... T>
    requires (std::convertible_to<T, double> && ...)
[[nodiscard]] double sum_readings(T... values) {
    return (0.0 + ... + static_cast<double>(values));
}

int main() {
    std::println("Total: {}", sum_readings(3, 4.5, 2));
    std::println("Empty total: {}", sum_readings());
}
