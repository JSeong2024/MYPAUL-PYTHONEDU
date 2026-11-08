#include <array>
#include <iostream>
#include <stdexcept>

int main() {
    const std::array<int, 3> voltages{12, 24, 48};
    const std::size_t index{3};

    if (index >= voltages.size()) {
        std::cout << "Index out of range: " << index << '\n';
    }
    try {
        const int value = voltages.at(index);
        std::cout << "Voltage: " << value << '\n';
    } catch (const std::out_of_range&) {
        std::cout << "at() rejected the index\n";
    }
}
