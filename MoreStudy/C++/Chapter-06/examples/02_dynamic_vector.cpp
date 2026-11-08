#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings;
    readings.reserve(5);
    readings.push_back(12);
    readings.push_back(18);
    readings.push_back(15);
    std::cout << "After reserve and insert: " << readings.size() << '\n';
    readings.resize(4);
    std::cout << "After resize: " << readings.size() << '\n';
    std::cout << "Fourth: " << readings.at(3) << '\n';
}
