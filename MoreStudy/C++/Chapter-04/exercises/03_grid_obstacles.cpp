#include <array>
#include <print>

int main() {
    constexpr std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0}
    };

    // TODO: traverse every cell with nested loops and count cells == 1.
    // Print "Obstacles: N".
    (void)grid;
    std::println("TODO: count obstacles");
}
