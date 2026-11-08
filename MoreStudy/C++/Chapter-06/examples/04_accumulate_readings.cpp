#include <array>
#include <iomanip>
#include <iostream>

int main() {
    const std::array<int, 5> samples{8, 12, 14, 10, 16};
    int total{};
    int minimum{samples.front()};
    int maximum{samples.front()};
    for (const int sample : samples) {
        total += sample;
        if (sample < minimum) minimum = sample;
        if (sample > maximum) maximum = sample;
    }
    const double average = static_cast<double>(total) / samples.size();
    std::cout << "Total: " << total << '\n';
    std::cout << "Min: " << minimum << '\n';
    std::cout << "Max: " << maximum << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Average: " << average << '\n';
}
