#include <array>
int main() {
    constexpr std::array<int,4> data{-2,4,0,7};
    if (sum_positive(data) != 11) return 1;
    constexpr std::array<int,0> empty{};
    return sum_positive(empty) == 0 ? 0 : 2;
}
