#include <print>
#include <utility>

struct MightThrow {
    MightThrow() = default;
    MightThrow(const MightThrow&) { std::println("Copy selected"); }
    MightThrow(MightThrow&&) noexcept(false) { std::println("Move selected"); }
};
struct SafeMove {
    SafeMove() = default;
    SafeMove(const SafeMove&) { std::println("Copy selected"); }
    SafeMove(SafeMove&&) noexcept { std::println("Move selected"); }
};

int main() {
    MightThrow a;
    SafeMove b;
    [[maybe_unused]] MightThrow a2{std::move_if_noexcept(a)};
    [[maybe_unused]] SafeMove b2{std::move_if_noexcept(b)};
}
