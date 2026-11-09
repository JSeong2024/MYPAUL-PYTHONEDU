#include <iostream>
#include <numeric>
#include <vector>
int main() {
    const std::vector<int> readings{12, 14, 16};
    std::cout << "Total: " << std::accumulate(readings.begin(), readings.end(), 0) << '\n';
}
