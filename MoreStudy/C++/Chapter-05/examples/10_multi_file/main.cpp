#include "inventory.hpp"
#include <iostream>

int main() {
    const auto stock{inventory::remaining_stock(25, 13)};
    if (!stock.has_value()) {
        std::cerr << "Error: invalid inventory data.\n";
        return 1;
    }
    std::cout << "Available: " << *stock << '\n';
}
