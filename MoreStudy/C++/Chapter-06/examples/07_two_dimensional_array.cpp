#include <array>
#include <iostream>

int main() {
    const std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0},
    };
    int blocked{};
    for (const auto& row : grid) {
        for (const int cell : row) {
            if (cell == 1) ++blocked;
        }
    }
    std::cout << "Rows: " << grid.size() << '\n';
    std::cout << "Columns: " << grid.front().size() << '\n';
    std::cout << "Blocked: " << blocked << '\n';
    std::cout << "Cell (1, 3): " << grid.at(1).at(3) << '\n';
}
