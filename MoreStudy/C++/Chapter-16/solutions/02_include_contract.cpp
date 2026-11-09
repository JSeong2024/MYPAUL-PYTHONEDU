#include <iostream>
#include <span>

[[nodiscard]] int sum_positive(std::span<const int> values) {
    int total = 0;
    for (int value : values) if (value > 0) total += value;
    return total;
}
#ifndef CH16_LIBRARY_ONLY
int main() { const int values[]{3,-2,5}; std::cout << sum_positive(values) << '\n'; }
#endif
