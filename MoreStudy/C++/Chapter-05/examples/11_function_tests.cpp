#include <iostream>

[[nodiscard]] constexpr int clamp_score(int score) noexcept {
    if (score < 0) {
        return 0;
    }
    if (score > 100) {
        return 100;
    }
    return score;
}

int main() {
    const bool passed = clamp_score(-10) == 0 &&
                        clamp_score(70) == 70 &&
                        clamp_score(150) == 100;
    if (!passed) {
        std::cerr << "Test failed\n";
        return 1;
    }
    std::cout << "All tests passed (3 cases)\n";
}
