#include <algorithm>
#include <print>

[[nodiscard]] constexpr int clamp_score(int score) noexcept {
    return std::clamp(score, 0, 100);
}

int main() {
    const bool tests_passed =
        clamp_score(-10) == 0 &&
        clamp_score(70) == 70 &&
        clamp_score(150) == 100;

    if (!tests_passed) {
        std::println("Test failed");
        return 1;
    }
    std::println("All tests passed (3 cases)");
}
