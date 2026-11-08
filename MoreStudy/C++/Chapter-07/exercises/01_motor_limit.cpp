#include <iostream>

[[nodiscard]] bool try_set_rpm(int& current, int requested) noexcept {
    // TODO: accept 0..3000; change current only if valid.
    (void)current;
    (void)requested;
    return false;
}

int main() {
    int rpm{1'200};
    const bool first{try_set_rpm(rpm, 2'500)};
    const bool second{try_set_rpm(rpm, 4'000)};
    std::cout << std::boolalpha;
    std::cout << "First: " << first << ", Second: " << second
              << ", RPM: " << rpm << '\n';
}
