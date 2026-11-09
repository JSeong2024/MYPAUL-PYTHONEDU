#include CH15_SOURCE_PATH
#include <array>
#include <cmath>
#include <limits>
#include <stdexcept>

static void check(bool test) { if (!test) throw std::runtime_error("test failed"); }
int main() {
    const std::array<int, 0> empty{};
    check(!ch15::analyze(empty));
    const std::array single{-5};
    const auto s = ch15::analyze(single);
    check(s && s->minimum == -5 && s->maximum == -5 && s->average == -5.0);
    const std::array values{-2, 0, 5};
    const auto result = ch15::analyze(values);
    check(result && result->minimum == -2 && result->maximum == 5);
    check(std::abs(result->average - 1.0) < 1e-12);
    const std::array limits{std::numeric_limits<int>::max(), std::numeric_limits<int>::max()};
    const auto big = ch15::analyze(limits);
    check(big && big->average == static_cast<double>(std::numeric_limits<int>::max()));
    std::cout << "PASS\n";
}
