#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 20) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::vector<int> readings;
    for (int i = 0; i < count; ++i) {
        int value{};
        if (!(std::cin >> value) || value < -100 || value > 100) {
            std::cerr << "Error: invalid input.\n";
            return 1;
        }
        readings.push_back(value);
    }
    int minimum{readings.front()};
    int maximum{readings.front()};
    int total{};
    for (int value : readings) {
        if (value < minimum) minimum = value;
        if (value > maximum) maximum = value;
        total += value;
    }
    std::cout << "Count: " << readings.size() << '\n';
    std::cout << "Min: " << minimum << '\n';
    std::cout << "Max: " << maximum << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Average: " << static_cast<double>(total) / readings.size() << '\n';
}
