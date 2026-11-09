#include <algorithm>
#include <iostream>
#include <unordered_set>
#include <vector>

int main() {
    const std::vector<int> ids{4, 2, 8, 2, 7};
    const std::unordered_set<int> lookup(ids.begin(), ids.end());
    const bool linear = std::find(ids.begin(), ids.end(), 7) != ids.end();
    const bool hashed = lookup.contains(7);  // C++20
    std::cout << std::boolalpha << "Vector found: " << linear
              << ", Hash found: " << hashed << "\n";
}
