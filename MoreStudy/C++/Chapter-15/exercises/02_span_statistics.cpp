#include <algorithm>
#include <array>
#include <iostream>
#include <optional>
#include <span>

namespace ch15 {
struct Stats { int minimum{}; int maximum{}; double average{}; };
[[nodiscard]] std::optional<Stats> analyze(std::span<const int> values) {
    // TODO: 빈 입력이면 std::nullopt 반환.
    //       그 외에는 최솟값·최댓값과 실수 평균을 구하세요.
    (void)values;
    return std::nullopt;
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const std::array data{10, 20, 30};
    if (const auto result = ch15::analyze(data)) {
        std::cout << "Min: " << result->minimum << ", Max: " << result->maximum
                  << ", Average: " << result->average << "\n";
    }
}
#endif
