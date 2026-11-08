#include <array>
#include <iostream>

int main() {
    const std::array<int, 4> readings{21, 24, 19, 23};
    std::cout << "Samples: " << readings.size() << '\n';
    std::cout << "First: " << readings.front() << '\n';
    std::cout << "Last: " << readings.back() << '\n';
}
