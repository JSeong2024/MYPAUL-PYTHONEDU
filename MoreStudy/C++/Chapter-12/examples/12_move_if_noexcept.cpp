#include <iostream>
#include <utility>

struct Fragile {
    Fragile() = default;
    Fragile(const Fragile&) { std::cout << "Copy\n"; }
    Fragile(Fragile&&) noexcept(false) { std::cout << "Move\n"; }
};

int main() {
    Fragile source;
    Fragile target{std::move_if_noexcept(source)};
    (void)target;
}
