#include <algorithm>
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> samples{3, -1, 8, 0, 4};
    auto nonnegative = samples | std::views::filter([](int value) { return value >= 0; });
    int total = 0;
    for (int value : nonnegative) total += value;
    std::cout << "Nonnegative sum: " << total << "\n";
}
