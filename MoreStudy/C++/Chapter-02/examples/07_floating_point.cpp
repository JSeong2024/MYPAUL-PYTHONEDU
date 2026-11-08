#include <iomanip>
#include <iostream>

int main() {
    const double sum{0.1 + 0.2};
    const double expected{0.3};

    std::cout << std::fixed << std::setprecision(17);
    std::cout << "Sum: " << sum << '\n';
    std::cout << "Expected: " << expected << '\n';

    std::cout << std::setprecision(2);
    std::cout << "Displayed: " << sum << '\n';
}
