#include <algorithm>
#include <iostream>
#include <span>
#include <vector>

namespace ch15 {
[[nodiscard]] std::vector<int> unique_sorted(std::span<const int> input) {
    // TODO: 입력 원본을 변경하지 않고, 오름차순 정렬 후 중복을 제거하세요.
    //       std::ranges::sort, std::unique, erase 등의 활용을 고려하세요.
    (void)input;
    return {};
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const std::vector input{4, 2, 4, 1, 2};
    const auto output = ch15::unique_sorted(input);
    std::cout << "Unique: " << output.size() << "\n";
}
#endif
