#include <print>
#include <utility>

struct Probe {
    Probe() = default;
    Probe(const Probe&) { std::println("Copy"); }
    Probe(Probe&&) noexcept { std::println("Move"); }
};

int main() {
    Probe source;
    Probe copied{source};
    Probe moved{std::move(source)};
    (void)copied;
    (void)moved;
}
