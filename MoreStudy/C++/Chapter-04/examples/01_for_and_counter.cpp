#include <iostream>

int main() {
    constexpr int sample_count{5};

    for (int number{1}; number <= sample_count; ++number) {
        std::cout << "Sample " << number << '\n';
    }

    std::cout << "Completed: " << sample_count << '\n';
}
