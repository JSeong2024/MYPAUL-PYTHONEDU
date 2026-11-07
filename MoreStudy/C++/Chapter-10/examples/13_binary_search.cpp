#include <iterator>
#include <algorithm>
#include <print>
#include <vector>

int main() {
    const std::vector<int> codes{10, 20, 20, 30, 40};  // 이미 정렬됨
    const auto lower = std::ranges::lower_bound(codes, 20);
    const auto upper = std::ranges::upper_bound(codes, 20);
    std::println("Has 30: {}", std::ranges::binary_search(codes, 30));
    std::println("Count of 20: {}", std::distance(lower, upper));
}
