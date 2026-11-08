#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 100) {
        std::cerr << "Error: N must be between 1 and 100.\n";
        return 1;
    }

    int total{};
    for (int number{1}; number <= n; ++number) {
        total += number;
    }

    std::cout << "Sum: " << total << '\n';
}
