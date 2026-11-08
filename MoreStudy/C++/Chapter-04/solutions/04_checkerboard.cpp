#include <iostream>

int main() {
    int rows{};
    int columns{};
    if (!(std::cin >> rows >> columns) ||
        rows < 1 || rows > 8 || columns < 1 || columns > 8) {
        std::cerr << "Error: rows and columns must be between 1 and 8.\n";
        return 1;
    }

    for (int row{0}; row < rows; ++row) {
        for (int column{0}; column < columns; ++column) {
            std::cout << ((row + column) % 2 == 0 ? '#' : '.');
        }
        std::cout << '\n';
    }
}
