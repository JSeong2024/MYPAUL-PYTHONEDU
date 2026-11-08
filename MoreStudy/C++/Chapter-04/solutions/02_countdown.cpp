#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 20) {
        std::cerr << "Error: N must be between 1 and 20.\n";
        return 1;
    }

    while (n > 0) {
        std::cout << n << '\n';
        --n;
    }
    std::cout << "Launch!\n";
}
