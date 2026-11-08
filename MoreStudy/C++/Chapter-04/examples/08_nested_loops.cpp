#include <iostream>

int main() {
    constexpr int rows{3};
    constexpr int columns{5};

    for (int row{0}; row < rows; ++row) {
        for (int column{0}; column < columns; ++column) {
            const char symbol{
                (row + column) % 2 == 0 ? '#' : '.'
            };
            std::cout << symbol;
        }
        std::cout << '\n';
    }
}
