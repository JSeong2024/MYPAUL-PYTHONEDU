#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings{20, -1, 18, -1, 25};
    const auto removed = std::erase(readings, -1);  // C++20

    std::cout << "Removed: " << removed << '\n';
    std::cout << "Remaining:";
    for (const int value : readings) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
