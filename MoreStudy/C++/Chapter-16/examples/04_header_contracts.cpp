#include <iostream>
#include <span>
#include <vector>
[[nodiscard]] int count(std::span<const int> items) {
    return static_cast<int>(items.size());
}
int main() {
    const std::vector<int> batch{7, 8, 9};
    std::cout << "Count: " << count(batch) << '\n';
}
