#include <algorithm>
#include <iostream>
#include <span>
#include <vector>

namespace ch15 {
[[nodiscard]] std::vector<int> unique_sorted(std::span<const int> input) {
    std::vector<int> result{input.begin(), input.end()};
    std::ranges::sort(result);
    result.erase(std::unique(result.begin(), result.end()), result.end());
    return result;
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const std::vector input{4, 2, 4, 1, 2};
    const auto output = ch15::unique_sorted(input);
    std::cout << "Unique: " << output.size() << "\n";
}
#endif
