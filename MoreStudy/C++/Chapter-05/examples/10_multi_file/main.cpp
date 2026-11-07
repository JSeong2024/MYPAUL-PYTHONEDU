#include "inventory.hpp"
#include <print>

int main() {
    const auto stock = inventory::remaining_stock(25, 13);
    if (!stock) {
        std::println("Invalid inventory data");
        return 1;
    }
    std::println("Available: {}", *stock);
}
