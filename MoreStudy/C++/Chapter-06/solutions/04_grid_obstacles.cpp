#include <algorithm>
#include <iostream>
#include <print>
#include <string>
#include <utility>
#include <vector>

int main() {
    int width{}, height{};
    if (!(std::cin >> width >> height) || width < 1 || width > 30 ||
        height < 1 || height > 30) {
        std::println(stderr, "Invalid grid size");
        return 1;
    }

    std::vector<std::string> grid;
    grid.reserve(static_cast<std::size_t>(height));
    for (int row = 0; row < height; ++row) {
        std::string line;
        if (!(std::cin >> line) || line.size() != static_cast<std::size_t>(width) ||
            !std::ranges::all_of(line, [](char c) { return c == '.' || c == '#'; })) {
            std::println(stderr, "Invalid grid row");
            return 1;
        }
        grid.push_back(std::move(line));
    }

    int blocked{};
    bool borders_clear{true};
    for (int row = 0; row < height; ++row) {
        for (int col = 0; col < width; ++col) {
            if (grid[static_cast<std::size_t>(row)][static_cast<std::size_t>(col)] == '#') {
                ++blocked;
                if (row == 0 || row == height - 1 || col == 0 || col == width - 1) {
                    borders_clear = false;
                }
            }
        }
    }

    std::println("Grid: {}x{}", width, height);
    std::println("Blocked: {}", blocked);
    std::println("Free: {}", width * height - blocked);
    std::println("All borders clear: {}", borders_clear ? "yes" : "no");
}
