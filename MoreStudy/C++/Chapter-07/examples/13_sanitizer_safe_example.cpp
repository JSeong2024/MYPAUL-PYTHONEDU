#include <array>
#include <iostream>
#include <span>

[[nodiscard]] int first_or_default(std::span<const int> samples,
                                   int fallback) noexcept {
    return samples.empty() ? fallback : samples.front();
}

int main() {
    const std::array<int, 3> samples{10, 20, 30};
    const std::span<const int> empty{};
    std::cout << "First: " << first_or_default(samples, -1) << '\n';
    std::cout << "Empty: " << first_or_default(empty, -1) << '\n';
}
