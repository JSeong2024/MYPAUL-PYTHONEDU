#include <iostream>
#include <span>

[[nodiscard]] int sum_positive(std::span<const int> values) {
    // TODO: 양수만 더해서 반환. 원본 Container를 복사하지 말 것.
    (void)values;
    return 0;
}
#ifndef CH16_LIBRARY_ONLY
int main() { const int values[]{3,-2,5}; std::cout << sum_positive(values) << '\n'; }
#endif
