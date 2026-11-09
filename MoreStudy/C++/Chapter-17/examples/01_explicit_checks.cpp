#include <iostream>
#include <stdexcept>
int clamp_reading(int value) {
    if (value < 0 || value > 100) throw std::invalid_argument("out of range");
    return value;
}
void expect(bool condition, const char* description) {
    if (!condition) throw std::runtime_error(description);
}
int main() {
    expect(clamp_reading(0) == 0, "lower boundary");
    expect(clamp_reading(100) == 100, "upper boundary");
    std::cout << "PASS: 2 checks\n";
}
