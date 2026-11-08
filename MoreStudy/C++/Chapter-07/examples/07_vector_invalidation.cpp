#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings{10, 20};
    const std::size_t selected_index{1};
    readings.push_back(30);
    if (selected_index < readings.size()) {
        // Do not reuse pointers or references saved before a possible reallocation.
        std::cout << "Selected: " << readings.at(selected_index) << '\n';
    }
    std::cout << "Size: " << readings.size() << '\n';
}
