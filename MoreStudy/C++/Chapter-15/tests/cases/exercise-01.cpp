#include CH15_SOURCE_PATH
#include <stdexcept>
#include <vector>

static void check(bool test) { if (!test) throw std::runtime_error("test failed"); }
int main() {
    check(ch15::make_squares(0).empty());
    check((ch15::make_squares(5) == std::vector<int>{0, 1, 4, 9, 16}));
    const auto large = ch15::make_squares(1000);
    check(large.size() == 1000 && large[999] == 998001);
    check(large.capacity() >= large.size());
    std::cout << "PASS\n";
}
