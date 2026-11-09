#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> readings{12, 18, 24, 30};
    const int total = std::accumulate(readings.begin(), readings.end(), 0);
    const auto peak = std::ranges::max_element(readings);
    std::cout << "Count: " << readings.size() << "\n";
    std::cout << "Total: " << total << ", Peak: " << *peak << "\n";
}
