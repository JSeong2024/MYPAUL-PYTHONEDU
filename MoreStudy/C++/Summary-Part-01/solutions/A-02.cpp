#include <iostream>
#include <string>

bool sell(long long& stock, long long quantity) {
    if (quantity < 1 || quantity > 100000 || quantity > stock) return false;
    stock -= quantity;
    return true;
}

bool restock(long long& stock, long long quantity) {
    if (quantity < 1 || quantity > 100000) return false;
    stock += quantity;
    return true;
}

int main() {
    long long stock = 0;
    int count = 0;
    if (!(std::cin >> stock >> count) || stock < 0 || stock > 100000 || count < 0) {
        std::cout << "INVALID\n";
        return 0;
    }
    for (int i = 0; i < count; ++i) {
        std::string command;
        long long quantity = 0;
        if (!(std::cin >> command >> quantity)) {
            std::cout << "INVALID\n";
            return 0;
        }
        const bool ok = command == "SELL" ? sell(stock, quantity)
                        : command == "RESTOCK" && restock(stock, quantity);
        std::cout << (ok ? "OK " : "FAIL ") << stock << '\n';
    }
}
