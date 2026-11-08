#include <algorithm>
#include <iostream>
#include <vector>

[[nodiscard]] std::vector<int> clean_readings(std::vector<int> readings) {
    std::erase(readings, -1);
    std::ranges::sort(readings);
    const auto duplicates = std::ranges::unique(readings);
    readings.erase(duplicates.begin(), duplicates.end());
    return readings;
}

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Error: invalid count\n";
        return 1;
    }
    std::vector<int> readings;
    readings.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        int value{};
        if (!(std::cin >> value) || value < -1 || value > 1'000) {
            std::cerr << "Error: invalid reading\n";
            return 1;
        }
        readings.push_back(value);
    }
    const auto cleaned = clean_readings(readings);
    if (cleaned.empty()) {
        std::cout << "EMPTY\n";
    } else {
        for (std::size_t i = 0; i < cleaned.size(); ++i) {
            if (i != 0) std::cout << ' ';
            std::cout << cleaned[i];
        }
        std::cout << '\n';
    }
}
