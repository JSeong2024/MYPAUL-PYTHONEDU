#include <iostream>

[[nodiscard]] bool try_set_rpm(int& current, int requested) noexcept {
    if (requested < 0 || requested > 3'000) {
        return false;
    }
    current = requested;
    return true;
}

int main() {
    int rpm{1'200};
    const bool first{try_set_rpm(rpm, 2'500)};
    const bool second{try_set_rpm(rpm, 4'000)};
    std::cout << std::boolalpha;
    std::cout << "First: " << first << '\n';
    std::cout << "Second: " << second << '\n';
    std::cout << "Motor: " << rpm << " RPM\n";
}
