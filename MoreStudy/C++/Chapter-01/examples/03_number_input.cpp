#include <iostream>

int main() {
    int quantity{};

    std::cout << "Quantity (1-1000): " << std::flush;
    if (!(std::cin >> quantity) || quantity < 1 || quantity > 1000) {
        std::cerr << "Error: enter an integer from 1 to 1000.\n";
        return 1;
    }

    std::cout << "Quantity: " << quantity << '\n';
    return 0;
}
