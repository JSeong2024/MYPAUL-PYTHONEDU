#include <iostream>

int main() {
    int items{};
    int capacity{};

    std::cout << "Items: " << std::flush;
    if (!(std::cin >> items)) {
        std::cerr << "Error: invalid box input.\n";
        return 1;
    }
    std::cout << "Capacity: " << std::flush;
    if (!(std::cin >> capacity) || items < 0 || capacity <= 0) {
        std::cerr << "Error: invalid box input.\n";
        return 1;
    }

    std::cout << "Full boxes: " << items / capacity << '\n';
    std::cout << "Remaining items: " << items % capacity << '\n';
}
