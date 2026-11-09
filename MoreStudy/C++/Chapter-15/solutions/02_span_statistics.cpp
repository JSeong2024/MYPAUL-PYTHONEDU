#include <algorithm>
#include <array>
#include <iostream>
#include <optional>
#include <span>

namespace ch15 {
struct Stats { int minimum{}; int maximum{}; double average{}; };
[[nodiscard]] std::optional<Stats> analyze(std::span<const int> values) {
    if (values.empty()) return std::nullopt;
    const auto [smallest, largest] = std::minmax_element(values.begin(), values.end());
    long long total = 0;
    for (const int value : values) total += value;
    return Stats{*smallest, *largest,
                 static_cast<double>(total) / static_cast<double>(values.size())};
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const std::array data{10, 20, 30};
    if (const auto result = ch15::analyze(data)) {
        std::cout << "Min: " << result->minimum << ", Max: " << result->maximum
                  << ", Average: " << result->average << "\n";
    }
}
#endif
