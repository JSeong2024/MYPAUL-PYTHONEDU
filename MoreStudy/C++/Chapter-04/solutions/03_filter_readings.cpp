#include <iomanip>
#include <iostream>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 8) {
        std::cerr << "Error: count must be between 1 and 8.\n";
        return 1;
    }

    int total{};
    int accepted{};
    for (int index{0}; index < count; ++index) {
        int reading{};
        if (!(std::cin >> reading) || reading < -100 || reading > 100) {
            std::cerr << "Error: reading must be between -100 and 100.\n";
            return 1;
        }
        if (reading < 0) {
            continue;
        }
        total += reading;
        ++accepted;
    }

    if (accepted == 0) {
        std::cerr << "Error: no accepted readings.\n";
        return 1;
    }

    const double average{
        static_cast<double>(total) / accepted
    };
    std::cout << "Accepted: " << accepted << '\n';
    std::cout << "Average: " << std::fixed
              << std::setprecision(1) << average << '\n';
}
