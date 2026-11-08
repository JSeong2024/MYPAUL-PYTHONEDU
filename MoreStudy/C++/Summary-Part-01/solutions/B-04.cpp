#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string code;
    long long price = 0;
    long long stock = 0;
};

const Product* find_product(const std::vector<Product>& items, const std::string& code) {
    for (const auto& product : items) {
        if (product.code == code) return &product;
    }
    return nullptr;
}

int main() {
    int count = 0;
    if (!(std::cin >> count) || count < 0 || count > 100) {
        std::cout << "INVALID\n";
        return 0;
    }
    std::vector<Product> items;
    for (int i = 0; i < count; ++i) {
        Product product;
        if (!(std::cin >> product.code >> product.price >> product.stock) ||
            product.price < 0 || product.stock < 0) {
            std::cout << "INVALID\n";
            return 0;
        }
        items.push_back(product);
    }
    std::string search_code;
    if (!(std::cin >> search_code)) {
        std::cout << "INVALID\n";
        return 0;
    }
    const Product* found = find_product(items, search_code);
    if (found == nullptr) std::cout << "NOT_FOUND\n";
    else std::cout << found->code << ' ' << found->price << ' ' << found->stock << '\n';
}
