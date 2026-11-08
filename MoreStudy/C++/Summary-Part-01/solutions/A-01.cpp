#include <iostream>

int main() {
    long long price = 0;
    long long percent = 0;
    if (!(std::cin >> price >> percent) || price < 0 || price > 1000000000LL ||
        percent < 0 || percent > 100) {
        std::cout << "INVALID\n";
        return 0;
    }
    // Multiply first in 64-bit arithmetic and round half up at the end.
    std::cout << (price * percent + 50) / 100 << '\n';
}
