#include <array>
#include <iostream>
#include <span>
#include <vector>

[[nodiscard]] long long total(std::span<const int> values) {
    long long result = 0;
    for (const int value : values) result += value;
    return result;
}
int main() {
    const std::array fixed{3, 5, 7};
    const std::vector dynamic{10, 20};
    std::cout << "Array: " << total(fixed) << ", Vector: " << total(dynamic) << "\n";
}
