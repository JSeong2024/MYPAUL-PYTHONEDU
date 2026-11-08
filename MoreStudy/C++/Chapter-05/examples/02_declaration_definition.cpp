#include <iostream>

int remaining_stock(int received, int shipped);  // Declaration

int main() {
    std::cout << "Remaining: " << remaining_stock(25, 13) << '\n';
}

int remaining_stock(int received, int shipped) {  // Definition
    return received - shipped;
}
