#include <iostream>
#include <limits>
[[nodiscard]] bool can_add(int lhs, int rhs) {
    if (rhs > 0) return lhs <= std::numeric_limits<int>::max() - rhs;
    if (rhs < 0) return lhs >= std::numeric_limits<int>::min() - rhs;
    return true;
}
int main() {
    std::cout << "Can add: " << std::boolalpha << can_add(9, 8) << '\n';
}
