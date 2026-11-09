#include <array>
#include <iostream>

int main() {
    const std::array<std::array<int, 3>, 2> matrix{{{{1, 2, 3}}, {{4, 5, 6}}}};
    int row_sum = 0;
    for (std::size_t row = 0; row < matrix.size(); ++row)
        for (std::size_t col = 0; col < matrix[row].size(); ++col)
            row_sum += matrix[row][col];
    int column_sum = 0;
    for (std::size_t col = 0; col < matrix[0].size(); ++col)
        for (std::size_t row = 0; row < matrix.size(); ++row)
            column_sum += matrix[row][col];
    std::cout << "Row-first: " << row_sum << ", Column-first: " << column_sum << "\n";
}
