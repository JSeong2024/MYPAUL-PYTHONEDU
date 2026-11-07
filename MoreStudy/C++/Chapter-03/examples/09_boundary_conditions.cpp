#include <iostream>
#include <print>

int main() {
    constexpr int battery_percent{20};

    if (battery_percent < 0 || battery_percent > 100) {
        std::cerr << "Error: battery percentage is out of range.\n";
        return 1;
    }

    if (battery_percent <= 20) {
        std::println("LOW BATTERY");
    } else if (battery_percent < 80) {
        std::println("NORMAL");
    } else {
        std::println("HIGH");
    }
}
