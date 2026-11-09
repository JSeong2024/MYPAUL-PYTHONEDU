#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> ids{9, 3, 12, 3, 5};
    std::ranges::sort(ids);
    const bool contains = std::binary_search(ids.begin(), ids.end(), 5);
    const auto range = std::equal_range(ids.begin(), ids.end(), 3);
    std::cout << std::boolalpha << "Has 5: " << contains
              << ", Count 3: " << (range.second - range.first) << "\n";
}
