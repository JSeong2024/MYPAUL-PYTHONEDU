#include <iostream>
#include <string>
#include <vector>

int main() {
    int width{};
    int height{};
    if (!(std::cin >> width >> height) || width < 1 || width > 20 || height < 1 || height > 20) {
        std::cerr << "Error: invalid grid.\n";
        return 1;
    }
    std::vector<std::string> grid;
    for (int row = 0; row < height; ++row) {
        std::string cells;
        if (!(std::cin >> cells) || cells.size() != static_cast<std::size_t>(width) ||
            cells.find_first_not_of(".#") != std::string::npos) {
            std::cerr << "Error: invalid grid.\n";
            return 1;
        }
        grid.push_back(cells);
    }
    int blocked{};
    bool border_clear{true};
    for (int row = 0; row < height; ++row) {
        for (int col = 0; col < width; ++col) {
            if (grid[row][col] != '#') continue;
            ++blocked;
            if (row == 0 || row == height - 1 || col == 0 || col == width - 1) {
                border_clear = false;
            }
        }
    }
    std::cout << "Blocked: " << blocked << '\n';
    std::cout << "Borders clear: " << (border_clear ? "yes" : "no") << '\n';
}
