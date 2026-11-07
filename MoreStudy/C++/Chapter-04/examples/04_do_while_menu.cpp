#include <iostream>
#include <limits>
#include <print>

int main() {
    int selection{};

    do {
        std::println("1. Show device status");
        std::println("0. Exit");
        std::cout << "Select: " << std::flush;

        if (!(std::cin >> selection)) {
            if (std::cin.eof()) {
                return 0;
            }
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::println("Invalid input");
            continue;
        }

        if (selection == 1) {
            std::println("Device: READY");
        } else if (selection != 0) {
            std::println("Unknown menu item");
        }
    } while (selection != 0);
}
