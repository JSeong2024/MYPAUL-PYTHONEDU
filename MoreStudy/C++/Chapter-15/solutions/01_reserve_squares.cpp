#include <cstddef>
#include <iostream>
#include <vector>

namespace ch15 {
[[nodiscard]] std::vector<int> make_squares(std::size_t count) {
    std::vector<int> result;
    result.reserve(count);
    for (std::size_t index = 0; index < count; ++index) {
        const int value = static_cast<int>(index);
        result.push_back(value * value);
    }
    return result;
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const auto values = ch15::make_squares(5);
    std::cout << "Count: " << values.size() << "\n";
    if (!values.empty()) std::cout << "Last: " << values.back() << "\n";
}
#endif
