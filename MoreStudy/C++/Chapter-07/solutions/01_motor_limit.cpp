#include <print>

[[nodiscard]] bool try_set_rpm(int& current, int requested) noexcept {
    if (requested < 0 || requested > 3'000) {
        return false;
    }
    current = requested;
    return true;
}

int main() {
    int current{1'000};
    const bool first = try_set_rpm(current, 2'500);
    const bool second = try_set_rpm(current, -10);
    std::println("First: {}, Second: {}, RPM: {}", first, second, current);
}
