#include <iomanip>
#include <iostream>

// TODO: 섭씨를 화씨로 변환하는 to_fahrenheit(double) 함수를 정의합니다.
// Formula: Fahrenheit = Celsius * 9 / 5 + 32

double to_fahrenheit(double celsius) {
    // TODO
    return celsius;
}

int main() {
    double celsius{};
    if (!(std::cin >> celsius)) {
        std::cerr << "Error: invalid temperature.\n";
        return 1;
    }
    std::cout << std::fixed << std::setprecision(1)
              << "Fahrenheit: " << to_fahrenheit(celsius) << '\n';
}
