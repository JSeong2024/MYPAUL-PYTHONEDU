#include <array>
#include <cstddef>
#include <print>

template <std::size_t Rows, std::size_t Columns>
struct Grid {
    static_assert(Rows > 0 && Columns > 0);
    std::array<int, Rows * Columns> cells{};

    [[nodiscard]] int& at(std::size_t row, std::size_t column) {
        return cells.at(row * Columns + column);
    }
};

int main() {
    Grid<3, 4> grid;
    grid.at(1, 2) = 9;
    std::println("Cell: {}", grid.at(1, 2));
    std::println("Elements: {}", grid.cells.size());
}
