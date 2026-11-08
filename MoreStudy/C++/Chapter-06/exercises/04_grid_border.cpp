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
    // TODO: 전체 장애물(#) 개수와 바깥 테두리에 장애물이 있는지 확인
    return 0;
}
