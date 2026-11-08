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

static_assert(clamp_score(-1) == 0);
static_assert(clamp_score(101) == 100);

int main() {
    std::cout << "Score: " << clamp_score(125) << '\n';
}
