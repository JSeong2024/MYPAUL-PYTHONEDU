#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> response_ms{18, 45, 22, 90};
    const auto slow = std::ranges::find_if(response_ms, [](int value) {
        return value >= 80;
    });
    const bool valid = std::ranges::all_of(response_ms, [](int value) {
        return value >= 0;
    });
    const auto high_count = std::ranges::count_if(response_ms, [](int value) {
        return value >= 40;
    });

    if (slow != response_ms.end()) {
        std::cout << "First slow: " << *slow << " ms\n";
    }
    std::cout << std::boolalpha << "All valid: " << valid << '\n';
    std::cout << "At least 40 ms: " << high_count << '\n';
}
