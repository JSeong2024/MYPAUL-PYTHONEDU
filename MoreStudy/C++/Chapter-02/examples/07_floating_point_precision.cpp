#include <cmath>
#include <print>

int main() {
    const double measured{0.1 + 0.2};
    constexpr double expected{0.3};
    constexpr double tolerance{1e-12};

    const bool equal_with_tolerance =
        std::abs(measured - expected) <= tolerance;

    std::println("Measured: {:.17f}", measured);
    std::println("Expected: {:.17f}", expected);
    std::println("Within tolerance: {}", equal_with_tolerance);
}
