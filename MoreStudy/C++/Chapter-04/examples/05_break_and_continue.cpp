#include <iostream>

int main() {
    for (int reading{-2}; reading <= 6; reading += 2) {
        if (reading < 0) {
            continue;
        }
        if (reading > 4) {
            std::cout << "Limit reached\n";
            break;
        }
        std::cout << "Accepted: " << reading << '\n';
    }
}
