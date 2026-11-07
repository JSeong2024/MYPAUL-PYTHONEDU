#include <print>

// 문제: requested가 0~3000 범위이면 current를 갱신하고 true를 반환.
// 범위를 벗어나면 current는 유지하고 false를 반환.
[[nodiscard]] bool try_set_rpm(int& current, int requested) noexcept {
    // TODO: 조건 검사와 참조 매개변수 갱신
    (void)current;
    (void)requested;
    return false;
}

int main() {
    int current{1'000};
    const bool first = try_set_rpm(current, 2'500);
    const bool second = try_set_rpm(current, -10);
    std::println("First: {}, Second: {}, RPM: {}", first, second, current);
}
