#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> raw{10, 20, 30};
    std::vector<int> calibrated;
    calibrated.reserve(raw.size());
    std::ranges::transform(raw, std::back_inserter(calibrated), [](int value) {
        return value + 2;
    });

    const long long total = std::accumulate(calibrated.begin(), calibrated.end(), 0LL);
    std::cout << "Calibrated:";
    for (const int value : calibrated) {
        std::cout << ' ' << value;
    }
    std::cout << "\nTotal: " << total << '\n';
}
