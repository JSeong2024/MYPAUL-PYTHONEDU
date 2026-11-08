#include <array>
#include <cstddef>
#include <iostream>

template <typename T, std::size_t N>
[[nodiscard]] T sum_fixed(const std::array<T, N>& items) {
    T sum{};
    for (const auto& item : items) sum += item;
    return sum;
}

int main() {
    const std::array numbers{2, 4, 6}; // CTAD: std::array<int, 3>
    std::cout << "Size: " << numbers.size() << '\n';
    std::cout << "Sum: " << sum_fixed(numbers) << '\n';
}
