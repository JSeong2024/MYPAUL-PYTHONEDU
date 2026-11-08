#include <iostream>

int main() {
    int selection{};

    do {
        std::cout << "1. Show status\n"
                  << "0. Exit\n"
                  << "Select: " << std::flush;

        if (!(std::cin >> selection)) {
            std::cerr << "Error: integer input required.\n";
            return 1;
        }

        if (selection == 1) {
            std::cout << "Status: READY\n";
        } else if (selection != 0) {
            std::cout << "Unknown selection\n";
        }
    } while (selection != 0);

    std::cout << "Goodbye\n";
}
