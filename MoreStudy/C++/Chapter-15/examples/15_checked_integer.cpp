#include <iostream>
#include <limits>
#include <optional>

[[nodiscard]] std::optional<long long> checked_add(long long a, long long b) {
    constexpr long long highest = std::numeric_limits<long long>::max();
    constexpr long long lowest = std::numeric_limits<long long>::min();
    if ((b > 0 && a > highest - b) || (b < 0 && a < lowest - b))
        return std::nullopt;
    return a + b;
}
int main() {
    const auto safe = checked_add(20, 30);
    const auto overflow = checked_add(std::numeric_limits<long long>::max(), 1);
    std::cout << "Safe: " << *safe << ", Overflow rejected: "
              << std::boolalpha << !overflow.has_value() << "\n";
}
