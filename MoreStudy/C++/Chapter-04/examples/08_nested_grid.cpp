#include <array>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0}
    };

    for (std::size_t row{0}; row < grid.size(); ++row) {
        for (std::size_t column{0}; column < grid[row].size(); ++column) {
            if (grid[row][column] == 1) {
                std::println("Obstacle: ({}, {})", row, column);
            }
        }
    }
}
