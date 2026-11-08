#include <concepts>
#include <iostream>
#include <type_traits>

template <typename T>
concept SafeReading = std::floating_point<T> && requires(T value) {
    { value + value } -> std::same_as<T>;
};

template <SafeReading T>
[[nodiscard]] T average(T first, T second) {
    return first + (second - first) / T{2};
}

static_assert(SafeReading<double>);
static_assert(!SafeReading<int>);

int main() {
    std::cout << "Average: " << average(4.0, 8.0) << '\n';
}
