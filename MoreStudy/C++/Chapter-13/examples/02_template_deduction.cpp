#include <concepts>
#include <print>

// 프로젝트의 측정 규칙: 두 실수 측정값 사이의 오차가 허용 범위 이내인가?
template <std::floating_point T>
[[nodiscard]] constexpr bool within_tolerance(T actual, T target, T tolerance) {
    return tolerance >= T{0} &&
           actual >= target - tolerance && actual <= target + tolerance;
}

static_assert(within_tolerance(10.1, 10.0, 0.2));
static_assert(!within_tolerance(10.5, 10.0, 0.2));

int main() {
    std::println("Temperature OK: {}", within_tolerance(24.7, 25.0, 0.5));
    std::println("Pressure OK: {}", within_tolerance<float>(1.02f, 1.0f, 0.05f));
    // within_tolerance(1.0, 1.0f, 0.1); // T 추론 불일치
}
