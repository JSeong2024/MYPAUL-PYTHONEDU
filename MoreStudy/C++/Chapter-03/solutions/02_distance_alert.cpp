#include <iostream>

int main() {
    int distance_cm{};
    std::cout << "Distance (0-400 cm): " << std::flush;
    if (!(std::cin >> distance_cm) || distance_cm < 0 || distance_cm > 400) {
        std::cerr << "Error: distance must be 0-400.\n";
        return 1;
    }
    if (distance_cm < 30) {
        std::cout << "STOP\n";
    } else if (distance_cm <= 100) {
        std::cout << "SLOW DOWN\n";
    } else {
        std::cout << "CLEAR\n";
    }
}
