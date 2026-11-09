#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings;
    readings.reserve(8);
    const int* const initial = readings.data();
    for (int index = 0; index < 8; ++index) readings.push_back(index * 2);
    std::cout << "Size: " << readings.size() << ", Capacity enough: "
              << std::boolalpha << (readings.capacity() >= 8) << "\n";
    std::cout << "Buffer unchanged: " << (readings.data() == initial) << "\n";
}
