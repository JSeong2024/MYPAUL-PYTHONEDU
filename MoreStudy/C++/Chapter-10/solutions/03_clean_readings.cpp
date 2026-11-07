#include <cstdio>
#include <algorithm>
#include <iostream>
#include <print>
#include <vector>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::println(stderr, "Invalid count");
        return 1;
    }
    std::vector<int> readings;
    readings.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        int value{};
        if (!(std::cin >> value) || value < -1 || value > 1'000) {
            std::println(stderr, "Invalid reading");
            return 1;
        }
        if (value != -1) readings.push_back(value);
    }
    std::ranges::sort(readings);
    const auto duplicates = std::ranges::unique(readings);
    readings.erase(duplicates.begin(), duplicates.end());
    if (readings.empty()) {
        std::println("EMPTY");
    } else {
        for (std::size_t i = 0; i < readings.size(); ++i) {
            if (i != 0) std::print(" ");
            std::print("{}", readings[i]);
        }
        std::println();
    }
}
