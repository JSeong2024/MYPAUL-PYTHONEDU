#include <array>
#include <print>

int main() {
    constexpr std::array grid{
        std::array{0, 1, 0, 0},
        std::array{0, 1, 1, 0},
        std::array{0, 0, 0, 0},
    };

    int blocked{};
    for (const auto& row : grid) {
        for (const int cell : row) {
            if (cell == 1) {
                ++blocked;
            }
        }
    }

    std::println("Rows: {}, Columns: {}", grid.size(), grid.front().size());
    std::println("Blocked cells: {}", blocked);
    std::println("Cell (1, 2): {}", grid.at(1).at(2));
}
