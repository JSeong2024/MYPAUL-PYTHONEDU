#include <iostream>

int main() {
    constexpr int max_attempts{3};

    for (int attempt{1}; attempt <= max_attempts; ++attempt) {
        std::cout << "Reading (0-100): " << std::flush;

        int reading{};
        if (!(std::cin >> reading)) {
            std::cerr << "Error: integer input required.\n";
            return 1;
        }

        if (reading < 0 || reading > 100) {
            std::cout << "Invalid reading\n";
            continue;
        }

        std::cout << "Accepted: " << reading << '\n';
        return 0;
    }

    std::cerr << "Error: retry limit exceeded.\n";
    return 1;
}
