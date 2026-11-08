#include <iostream>

int main() {
    int battery_percent{};
    std::cout << "Battery (0-100): " << std::flush;
    if (!(std::cin >> battery_percent)) {
        std::cerr << "Error: enter a battery percentage.\n";
        return 1;
    }
    if (battery_percent < 0 || battery_percent > 100) {
        std::cerr << "Error: battery percentage must be 0-100.\n";
        return 1;
    }

    std::cout << "Accepted: " << battery_percent << "%\n";
}
