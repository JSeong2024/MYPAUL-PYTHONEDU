#include <iostream>
#include <stdexcept>
[[nodiscard]] int normalized(int reading) {
    if (reading < 0 || reading > 100) throw std::invalid_argument("reading out of range");
    return reading;
}
int main() {
    if (normalized(35) != 35) return 1; // Release에서도 검사 유지
    std::cout << "Test: PASS\n";
}
