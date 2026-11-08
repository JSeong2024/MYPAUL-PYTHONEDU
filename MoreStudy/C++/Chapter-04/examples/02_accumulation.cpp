#include <iomanip>
#include <iostream>

int main() {
    constexpr int sample_count{4};
    int total{0};

    for (int number{1}; number <= sample_count; ++number) {
        const int reading{number * 10};
        total += reading;
    }

    const double average{
        static_cast<double>(total) / sample_count
    };

    std::cout << "Total: " << total << '\n';
    std::cout << "Average: " << std::fixed
              << std::setprecision(1) << average << '\n';
}
