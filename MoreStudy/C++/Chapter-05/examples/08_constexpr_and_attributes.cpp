#include <print>

[[nodiscard]] constexpr int clamp_percentage(int value) noexcept {
    if (value < 0) {
        return 0;
    }
    if (value > 100) {
        return 100;
    }
    return value;
}

static_assert(clamp_percentage(-5) == 0);
static_assert(clamp_percentage(120) == 100);

int main() {
    const int measured_quality{127};
    std::println("Quality: {}%", clamp_percentage(measured_quality));
}
