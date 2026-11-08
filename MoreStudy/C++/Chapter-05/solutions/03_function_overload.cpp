#include <iostream>

void show_reading(int value) {
    std::cout << "Count: " << value << '\n';
}

void show_reading(double value) {
    std::cout << "Temperature: " << value << " C\n";
}

int main() {
    show_reading(12);
    show_reading(23.5);
}
