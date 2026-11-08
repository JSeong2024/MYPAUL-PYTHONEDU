#include <iostream>

int delivery_fee(int weight, int express) {
    const int extra_weight = weight > 1000 ? weight - 1000 : 0;
    const int blocks = (extra_weight + 499) / 500;
    return 3000 + blocks * 500 + (express == 1 ? 2000 : 0);
}

int main() {
    int weight = 0;
    int express = 0;
    if (!(std::cin >> weight >> express) || weight < 1 || weight > 20000 ||
        (express != 0 && express != 1)) {
        std::cout << "INVALID\n";
        return 0;
    }
    std::cout << delivery_fee(weight, express) << '\n';
}
