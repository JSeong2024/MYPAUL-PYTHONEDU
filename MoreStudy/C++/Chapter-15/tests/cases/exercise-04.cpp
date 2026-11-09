#include CH15_SOURCE_PATH
#include <array>
#include <stdexcept>
#include <vector>

static void check(bool test) { if (!test) throw std::runtime_error("test failed"); }
int main() {
    const std::vector input{4, 2, 4, 1, 2};
    const auto copy = input;
    check((ch15::unique_sorted(input) == std::vector<int>{1, 2, 4}));
    check(input == copy);
    const std::array<int, 0> empty{};
    check(ch15::unique_sorted(empty).empty());
    const std::array negatives{-3, -3, -1, 0, 2, -1};
    check((ch15::unique_sorted(negatives) == std::vector<int>{-3, -1, 0, 2}));
    std::cout << "PASS\n";
}
