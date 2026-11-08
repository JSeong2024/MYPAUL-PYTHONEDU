#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> delays{42, 18, 31, 18, 55};
    const auto high = std::ranges::count_if(delays, [](int value) { return value >= 40; });
    const long long total = std::accumulate(delays.begin(), delays.end(), 0LL);
    std::ranges::sort(delays);
    std::cout << "Total: " << total << '\n';
    std::cout << "Slow: " << high << '\n';
    std::cout << std::boolalpha;
    std::cout << "Has 31: " << std::ranges::binary_search(delays, 31) << '\n';
    std::cout << "First sorted: " << delays.front() << '\n';
}
