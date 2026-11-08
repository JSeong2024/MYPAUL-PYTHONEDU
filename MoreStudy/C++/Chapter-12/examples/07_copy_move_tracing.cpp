#include <iostream>
#include <utility>

struct Probe {
    Probe() = default;
    Probe(const Probe&) { std::cout << "Copy\n"; }
    Probe(Probe&&) noexcept { std::cout << "Move\n"; }
};

int main() {
    Probe source;
    Probe copied{source};
    Probe moved{std::move(source)};
    (void)copied;
    (void)moved;
}
