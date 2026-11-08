#include <iostream>

template <typename T>
[[nodiscard]] bool within_tolerance(T measured, T target, T tolerance) {
    return tolerance >= T{} && measured >= target - tolerance &&
           measured <= target + tolerance;
}

int main() {
    std::cout << std::boolalpha;
    std::cout << "Integer: " << within_tolerance(97, 100, 5) << '\n';
    std::cout << "Double: " << within_tolerance(19.8, 20.0, 0.5) << '\n';
    std::cout << "Explicit: " << within_tolerance<double>(9, 10.0, 0.2) << '\n';
}
