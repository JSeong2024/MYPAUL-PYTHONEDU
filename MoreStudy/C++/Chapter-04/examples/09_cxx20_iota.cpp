#include <iostream>
#include <ranges>

int main() {
    for (const int number : std::views::iota(1, 5)) {
        std::cout << "Step " << number << '\n';
    }
}
