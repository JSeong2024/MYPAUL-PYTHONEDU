#include <algorithm>
#include <print>

[[nodiscard]] int clamp_rpm(int requested) noexcept {
    return std::clamp(requested, 0, 3'000);
}

void update_rpm(int& current, int requested) noexcept {
    current = clamp_rpm(requested);
}

int main() {
    int motor_rpm{1'200};
    update_rpm(motor_rpm, 3'500);
    std::println("Motor: {} RPM", motor_rpm);
}
