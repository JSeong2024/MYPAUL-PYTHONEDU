#include <iostream>
#include <optional>

std::optional<int> shipping_fee(int subtotal, int remote) {
    if (subtotal < 0 || (remote != 0 && remote != 1)) {
        return std::nullopt;
    }
    const int base{subtotal >= 50000 ? 0 : 3000};
    return base + (remote == 1 ? 2000 : 0);
}

int main() {
    int subtotal{};
    int remote{};
    if (!(std::cin >> subtotal >> remote)) {
        std::cerr << "Error: invalid order.\n";
        return 1;
    }
    const auto fee{shipping_fee(subtotal, remote)};
    if (!fee.has_value()) {
        std::cerr << "Error: invalid order.\n";
        return 1;
    }
    std::cout << "Shipping: " << *fee << " won\n";
}
