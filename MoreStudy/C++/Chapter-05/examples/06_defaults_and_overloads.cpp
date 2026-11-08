#include <iostream>

int shipping_fee(int order_won, int base_fee = 3000) {
    return order_won >= 50000 ? 0 : base_fee;
}

void show_value(int value) {
    std::cout << "Count: " << value << '\n';
}

void show_value(double value) {
    std::cout << "Temperature: " << value << " C\n";
}

int main() {
    std::cout << "Shipping: " << shipping_fee(42000) << " won\n";
    std::cout << "Custom shipping: " << shipping_fee(42000, 4500) << " won\n";
    show_value(12);
    show_value(23.5);
}
